import pathlib
import datajoint as dj
import djsciops.axon as dj_axon
import djsciops.settings as dj_settings
import djsciops.authentication as dj_auth


LOCAL_OUTBOX = pathlib.Path(R"E:/uploads")
LOCAL_INBOX = pathlib.Path(R"E:/kilosort/axon")
PROJECT_NAME = "utah-organoids"


config = dj_settings.get_config()
s3_session = dj_auth.Session(
    aws_account_id=config["aws"]["account_id"],
    s3_role=config["s3"]["role"],
    auth_client_id=config["djauth"]["client_id"],
)
s3_bucket = config["s3"]["bucket"]


def upload_session_data(session_dir_relpath):
    session_dir_relpath = pathlib.Path(session_dir_relpath).as_posix()

    local_session_dir = LOCAL_OUTBOX / session_dir_relpath
    assert local_session_dir.exists(), f"{local_session_dir} does not exist"
    assert local_session_dir.is_dir(), f"{local_session_dir} is not a directory"

    dj_session_dir = f"{PROJECT_NAME}/inbox/{session_dir_relpath}/"
    dj_axon.upload_files(
        source=local_session_dir.as_posix(),
        destination=dj_session_dir,
        session=s3_session,
        s3_bucket=s3_bucket,
    )
