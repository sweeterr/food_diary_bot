import logging
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import Config
from record import Record


def get_creds(configs: Config):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", configs.google["scopes"])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


def get_sheet_title(service, configs):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=configs.google["spreadsheet_id"]).execute()
    title = sheet_metadata.get("properties").get("title")
    return title


def update_sheet(record: Record, test=True):
    configs = Config()
    creds = get_creds(configs)
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)
    values = [record.row]
    body = {"values": values}
    if test:
        sheet_range = configs.google["test_sheet_name"]
    else:
        sheet_range = configs.google["prod_sheet_name"]
    result = service.spreadsheets().values().append(
        spreadsheetId=configs.google["spreadsheet_id"], range=sheet_range,
        valueInputOption="RAW", body=body).execute()
    sheet_title = get_sheet_title(service, configs)
    logging.info(f"Google doc '{sheet_title}', sheet '{sheet_range}' updated "
                 f"with {result.get('updates').get('updatedCells')} values: "
                 f"{' '.join(values[0])}.")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    record = Record("tvorog", "food")
    update_sheet(record, test=True)



if __name__ == "__main__":
    main()