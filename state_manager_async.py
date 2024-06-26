// The given PowerShell script is written in Python and utilizes the Azure Storage File Share API to store state information for a function app using asynchronous I/O operations (aio).
// This script helps to perform health checks on specified function applications, and to confirm persistence on asychronus tasks within Azure Storage Service



Purpose: This class StateManagerAsync provides an interface allowing functions: - To write marker text indicating their current status - And read back that data when needed

from azure.storage.fileshare.aio import ShareClient
from azure.storage.fileshare.aio import ShareFileClient
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError


class StateManagerAsync:
    def __init__(self, connection_string, share_name='funcstatemarkershare', file_path='funcstatemarkerfile'):
        self.connection_string = connection_string
        self.share_name = share_name
        self.file_path = file_path

    def _get_file_cli(self):
        return ShareFileClient.from_connection_string(conn_str=self.connection_string, share_name=self.share_name, file_path=self.file_path)

    def _get_share_cli(self):
        return ShareClient.from_connection_string(conn_str=self.connection_string, share_name=self.share_name)

    async def post(self, marker_text: str):
        file_cli = self._get_file_cli()
        async with file_cli:
            try:
                await file_cli.upload_file(marker_text)
            except ResourceNotFoundError:
                share_cli = self._get_share_cli()
                async with share_cli:
                    try:
                        await share_cli.create_share()
                    except ResourceExistsError:
                        pass
                    await file_cli.upload_file(marker_text)

    async def get(self):
        file_cli = self._get_file_cli()
        async with file_cli:
            try:
                cor = await file_cli.download_file()
                f = await cor.readall()
                return f.decode()
            except ResourceNotFoundError:
                return None
