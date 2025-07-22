from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "documentmanagement")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseUploadError(Exception):
    pass


def upload_to_supabase(file, folder):
    path = f"{folder}/{file.name}"

    print("file", file)

    file_content = file.read()
    file.seek(0)

    try:
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=path,
            file=file_content,
            file_options={"content-type": file.content_type},
        )
        print("response--------", response)
    except Exception as e:
        print("Upload failed:", e)
        raise SupabaseUploadError("Upload to Supabase failed") from e

    public_url_data = supabase.storage.from_(
        SUPABASE_BUCKET).get_public_url(path)
    
    print("public_url_data---------", public_url_data)
    return public_url_data
