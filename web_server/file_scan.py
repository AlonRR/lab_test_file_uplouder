# Need a scan function here, that is called by app.py after file upload
# once the file is scanned it can be uploaded to S3 using file_upload.py to either
# the quarantine or production bucket based on scan results.
# if the file is clean upload to production bucket
# if the file is infected upload to quarantine bucket and send alert email using email_alert.py
# placeholder for file scanning functionality
