import io
import json
import logging
import os

import requests

# Handle JSON List and send as messages to SumoLogic
def handler(ctx, data: io.BytesIO = None):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Sumologic endpoint URL to upload OCI logs to HTTP custom app.
    # this value will be defined defined in func.yaml
    sumologic_endpoint = os.environ['SUMOLOGIC_ENDPOINT']
    debug = True if os.environ['DEBUG'].casefold() == "true" else False
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Function start")

    # If the following is added, the function returns the request, so that SCH can send to actual target

    try:
        logentries = json.loads(data.getvalue()) # deserialize the bytesstream input as JSON array
        if not isinstance(logentries, list):
            logger.debug(f'JSON entry from Event: {logentries}')
            try:
                response_from_sumologic = requests.post(sumologic_endpoint,
                                                    json=logentries,
                                                    headers={})
                logging.getLogger().debug(f"From Sumo: {response_from_sumologic}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTPError: {e.errno}")
            return
        else:
            # Optional...log the input to the function as human readble JSON. 
            # Not to be used in production
            logger.debug(f"JSON list from SCH - Logs to process: {len(logentries)}")

            for logEntry in logentries: 
                logger.debug(f"Log Entry JSON: {logEntry}")
                # Post the JSON as-is with no headers
                # Try and eat error
                try:
                    response_from_sumologic = requests.post(sumologic_endpoint,
                                                        json=logEntry,
                                                        headers={})
                    logging.getLogger().debug(f"From Sumo: {response_from_sumologic}")
                except requests.exceptions.HTTPError as e:
                    logger.error(f"HTTPError: {e.errno}")

            logger.debug("function end - No return")
            return

    except Exception as e:
        logger.error("Failure in the function: {}".format(str(e)))
        return

