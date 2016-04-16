def app(environ, start_response):
    result = [environ['wsgi.input'].read()]
    result = result + [environ['QUERY_STRING']]
    result = result + [' '] + [environ['REQUEST_METHOD']]
    result = result + ["<form name='form' method='POST' action='http://127.0.0.1/'><input type='text' name='lorem'><input type='submit'></form>"]
    status = '200 OK'
    response_headers = [
        ('Content-type','text/html')
    ]
    start_response(status, response_headers)
    return result
