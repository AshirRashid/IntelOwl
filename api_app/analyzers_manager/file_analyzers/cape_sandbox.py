# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

import logging
import time

import requests

from api_app.analyzers_manager.classes import FileAnalyzer
from api_app.analyzers_manager.exceptions import AnalyzerRunException
from tests.mock_utils import MockUpResponse, if_mock_connections, patch

logger = logging.getLogger(__name__)


class CAPEsandbox(FileAnalyzer):
    class ContinuePolling(Exception):
        pass

    _api_key_name: str
    VM_NAME: str
    max_tries: int
    poll_distance: int
    _url_key_name: str

    def config(self):
        super().config()
        self.__session = requests.Session()
        self.__session.headers = {
            "Authorization": f"Token {self._api_key_name}",
        }

    def run(self):
        api_url: str = self._url_key_name + "/apiv2/tasks/create/file/"
        to_respond = {}

        logger.info(f"Job: {self.job_id} -> " "Starting file upload.")
        data = {}
        if self.VM_NAME:
            data["machine"] = self.VM_NAME

        try:
            response = self.__session.post(
                api_url,
                files={
                    "file": (self.filename, self.read_file_bytes()),
                },
                data=data,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise AnalyzerRunException(e)

        response_json = response.json()
        logger.debug(f"response received: {response_json}")
        response_error = response_json.get("error", False)

        if not response_error:
            to_respond["result_url"] = response_json.get("url")
            task_id = response_json.get("data").get("task_ids")[0]
            result = self.__poll_for_result(task_id=task_id)
            to_respond["response"] = result

            logger.info(
                f"Job: {self.job_id} -> "
                "File uploaded successfully without any errors."
            )

        else:
            response_errors = response_json.get("errors", [])
            if response_errors:
                values = list(response_errors[0].values())
                if (
                    values
                    and values[0]
                    == "Not unique, as unique option set on submit or in conf/web.conf"
                ):

                    #    The above response is only returned when
                    #    a sample that has been already
                    #    uploaded once is uploaded again.

                    #    If it has been then we can just check it's
                    #    report by querying the CAPESandbox API with the md5 hash of
                    #    the file.

                    #    If it exists in their database and is readable by us,
                    #    the following code further fetches it's information.
                    #    response_json in this case should look somewhat like this:

                    # {
                    #    'error': True,
                    #    'error_value': 'Error adding task to database',
                    #    'errors': [{
                    #        'filename.exe':
                    #           'Not unique, as unique option set
                    #           on submit or in conf/web.conf'
                    #    }]
                    # }

                    logger.info(
                        f"Job: {self.job_id} -> "
                        "File uploaded is already present in the database. "
                        "Querying its information through it's md5 hash.."
                    )

                    status_id = self.__search_by_md5()
                    gui_report_url = self._url_key_name + "/submit/status/" + status_id
                    report_url = (
                        self._url_key_name
                        + "/apiv2/tasks/get/report/"
                        + status_id
                        + "/json"
                    )
                    to_respond["result_url"] = gui_report_url

                    try:
                        final_request = self.__session.get(
                            report_url,
                        )
                    except requests.RequestException as e:
                        raise AnalyzerRunException(e)

                    to_respond["response"] = final_request.json()

        return to_respond

    def __search_by_md5(self) -> str:
        db_search_url = self._url_key_name + "/apiv2/tasks/search/md5/" + self.md5

        try:
            q = self.__session.get(db_search_url)
            q.raise_for_status()

        except requests.RequestException as e:
            raise AnalyzerRunException(e)

        data_list = q.json().get("data")
        if not data_list:
            raise AnalyzerRunException(
                "'data' key in response isn't populated in __search_by_md5 as expected"
            )

        status_id_int = data_list[0].get("id")
        status_id = str(status_id_int)
        return status_id

    def __poll_for_result(
        self,
        task_id,
    ) -> dict:
        results = None
        status_api = self._url_key_name + "/apiv2/tasks/status/" + str(task_id)
        for try_ in range(self.max_tries):
            attempt = try_ + 1
            try:
                logger.info(
                    f" Job: {self.job_id} -> "
                    f"Starting poll number #{attempt}/{self.max_tries}"
                )
                try:
                    request = self.__session.get(status_api)
                    # 429 Rate Limit is caught by the raise_for_status
                    request.raise_for_status()
                except requests.RequestException as e:
                    raise self.ContinuePolling(f"RequestException {e}")

                # in case the request was ok
                responded_json = request.json()
                error = responded_json.get("error")
                data = responded_json.get("data")

                logger.info(
                    f"Job: {self.job_id} -> " f"Status of the CAPESandbox task: {data}"
                )

                if error:
                    raise AnalyzerRunException(error)

                if data in ("pending", "running", "processing"):
                    raise self.ContinuePolling(f"Task still {data}")

                if data in ("reported", "completed"):
                    report_url = (
                        self._url_key_name
                        + "/apiv2/tasks/get/report/"
                        + str(task_id)
                        + "/json"
                    )
                    try:
                        final_request = self.__session.get(
                            report_url,
                        )
                        final_request.raise_for_status()
                    except requests.RequestException as e:
                        raise AnalyzerRunException(e)

                    logger.info(
                        f" Job: {self.job_id} ->"
                        f"Poll number #{attempt}/{self.max_tries} fetched"
                        " the results of the analysis."
                        " stopping polling.."
                    )

                    results = final_request.json()
                    break

                else:
                    raise AnalyzerRunException(
                        f"status {data} was unexpected. Check the code"
                    )

            except self.ContinuePolling as e:
                logger.info(
                    f"Job: {self.job_id} -> "
                    "Continuing the poll at attempt number: "
                    f"#{attempt}/{self.max_tries}. {e}. "
                    f"Sleeping for {self.poll_distance} seconds."
                )
                last_try = self.max_tries - 1
                if try_ != last_try:  # avoiding useless last sleep
                    time.sleep(self.poll_distance)

        if not results:
            raise AnalyzerRunException(f"{self.job_id} poll ended without results")
        return results

    @classmethod
    def _monkeypatch(cls):
        patches = [
            if_mock_connections(
                patch(
                    "requests.Session.get",
                    return_value=MockUpResponse(
                        {"error": False, "data": "completed"}, 200
                    ),
                ),
                patch(
                    "requests.Session.post",
                    return_value=MockUpResponse(
                        {
                            "error": False,
                            "data": {
                                "task_ids": [1234],
                            },
                            "errors": [],
                            "url": ["http://fake_url.com/submit/status/1234/"],
                        },
                        200,
                    ),
                ),
            )
        ]
        return super()._monkeypatch(patches=patches)
