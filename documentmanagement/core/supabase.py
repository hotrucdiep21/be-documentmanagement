from supabase import create_client
import os
from dotenv import load_dotenv
import uuid
from urllib.parse import urlparse

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "documentmanagement")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseUploadError(Exception):
    pass


def upload_to_supabase(file, folder, previous_url=None):
    if previous_url and SUPABASE_URL in previous_url:
        try:
            relative_path = get_relative_path_from_url(previous_url)
            if relative_path:
                supabase.storage.from_(SUPABASE_BUCKET).remove([relative_path])
                print("delete old file:", relative_path)
            else:
                print("Could not parse relative path from previous_url")
        except Exception as e:
            print("Fail to delete old file: ", e)

    file_ext = file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    path = f"{folder}/{filename}"

    try:
        file_content = file.read()
        file.seek(0)

        response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=path,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        print("response-------", response)
    except Exception as e:
        print("Upload failed: ", e)
        raise SupabaseUploadError("Upload to Supabase failed") from e

    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)
    print(public_url)
    return public_url


def get_relative_path_from_url(url):
    parsed = urlparse(url)
    path = parsed.path
    prefix = f"/storage/v1/object/public/{SUPABASE_BUCKET}/"
    if prefix in path:
        return path.split(prefix)[-1]
    return None
