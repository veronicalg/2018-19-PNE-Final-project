
import http.server
import socketserver
import termcolor
import json
import http.client

# Define the Server's port
PORT = 8005
HOSTNAME = "rest.ensembl.org"

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print ("Prueba", self.path)
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the client, depending on the resource
        if self.path == "/":
            with open ("webpage.html", "r") as f:
                contents = f.read()

        elif self.path[0:12] == "/listSpecies":


            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request("GET", "/info/species?content-type=application/json")
            r1 = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)

            # -- Read the response's body and close
            # -- the connection
            text_json = r1.read().decode("utf-8") #En string format
            conn.close()

            list = json.loads(text_json) #Json format
            #print("The list is: ", list)


            list = list['species']
            print(list)

            if "limit" in self.path:
                limit = self.path.split("=")[1]

                print("LIMIT:", limit)
            else:
                limit = len(list)

            #for i in list:
                #print(i['display_name'])

            contents="""
            <html>
            <body>
            <ol>"""
            count=0
            for i in list:
                contents= contents+"<li>"+i['display_name']+"</li<br>"
                count= count+1
                if str(count)==limit:
                    print(count)
                    break
                #print(count)

            contents=contents+"""</ol> 
            </body>
            </html>
            """

        elif self.path[0:10]=="/karyotype":
            print("HOLA")

            specie = self.path.split("=")[1]
            print(specie)
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request("GET", "/info/assembly/"+specie+"?content-type=application/json")
            r1 = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)

            # -- Read the response's body and close
            # -- the connection
            text_json = r1.read().decode("utf-8") #En string format
            conn.close()

            response = json.loads(text_json)
            print(response)

            karyotype_list=response['karyotype']

            contents = """
                       <html>
                       <body>
                       <ul>"""
            count = 0
            for i in karyotype_list:
                contents = contents + "<li>" + i + "</li<br>"

            contents = contents + """</ul> 
                       </body>
                       </html>
                       """

        elif self.path [0:17] == "/chromosomeLength":
            chromo= self.path.split("=")[2]
            second_str = self.path.split("=")[1]
            specie = second_str.split("&")[0]
            print("Chromo; ", chromo)
            print("Specie:", specie)

            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request("GET", "/info/assembly/"+specie+"?content-type=application/json")
            r1 = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)

            # -- Read the response's body and close
            # -- the connection
            text_json = r1.read().decode("utf-8")  # En string format
            conn.close()

            response = json.loads(text_json)
            print(response)

            list = response['top_level_region']

            length = 0
            for i in list:
                if i['name']==chromo:
                    length = i['length']
            print(length)

            contents = """
                                  <html>
                                  <body>
                                  <ul>"""

            contents = contents + "<li>" + str(length) + "</li<br>"

            contents = contents + """</ul> 
                                  </body>
                                  </html>
                                  """


        else:
            with open("error.html", "r") as f:
                contents = f.read()

        print(self.requestline)


        # Generating the response message
        self.send_response(200)  # -- Status line: OK! #El navegador va a ser contestado.

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html') #Código en formato html.
        self.send_header('Content-Length', len(str.encode(contents))) #Conocer numero de bytes codificados.

        # The header is finished
        self.end_headers() #3

        # Send the response message
        self.wfile.write(str.encode(contents)) #--Enviar el contenido.

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler
socketserver.TCPServer.allow_reuse_address = True

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")