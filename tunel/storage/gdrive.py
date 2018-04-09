from apiclient import discovery
from tunel.utils import get_credentials
from apiclient.http import (
    MediaIoBaseDownload, 
    MediaFileUpload
)

def fetch(query, sort='modifiedTime desc'):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    results = service.files().list(q=query,orderBy=sort,
                                   pageSize=10,
                                   fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items

def download_file(file_id, output_file):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    #file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
    request = service.files().export_media(fileId=file_id,mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #request = service.files().get_media(fileId=file_id)

    fh = open(output_file,'wb') #io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        #print ("Download %d%%." % int(status.progress() * 100))
    fh.close()
    #return fh

def update_file(file_id, local_file):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    # First retrieve the file from the API.
    file = service.files().get(fileId=file_id).execute()
    # File's new content.
    media_body = MediaFileUpload(local_file, resumable=True)
    # Send the request to the API.
    updated_file = service.files().update(fileId=file_id,
                                          #body=file,
                                          #newRevision=True,
                                          media_body=media_body).execute()
