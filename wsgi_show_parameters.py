from pprint import pformat

def application(environ, start_response):
  status = '200 OK'

  output = [b'<pre>']
  output = [b'\n\nGET parameters:\n' + environ['QUERY_STRING'].encode('utf-8')]

  output.append(b'</pre>')

  output.append(b'\n\n<form method="post">')
  output.append(b'<input type="text" name="test">')
  output.append(b'<input type="submit">')
  output.append(b'</form>')

  if environ['REQUEST_METHOD'] == 'POST':
    output.append(b'\n<pre>')
    output.append(b'POST parameters: ')
    output.append(pformat(environ['wsgi.input'].read()).encode('utf-8'))
    output.append(b'</pre>')

  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  return output


app = application
