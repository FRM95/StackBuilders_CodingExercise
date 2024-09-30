from requests import get, exceptions

# Get response from an endpoint
def getRequest(endpoint:str, **kwargs):
    try:
        request = get(url=endpoint, **kwargs)
        request.raise_for_status()
    except exceptions.HTTPError as ex:
        return f'GET HTTPError exception: {ex}'
    except exceptions.ConnectionError as ex:
        return f'GET ConnectionError exception: {ex}'
    except exceptions.Timeout as ex:
        return f'GET Timeout exception: {ex}'
    except exceptions.RequestException as ex:
        return f'GET Request exception: {ex}'
    except Exception as ex:
        return f'GET Unhandled exception: {ex}'
    else:
        return request