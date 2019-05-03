# Server for final practice. (Basic, medium and advanced level)
import http.server
import socketserver
import termcolor
import json
import http.client
from Seq import Seq


# Define the Server's port
PORT = 8000
HOSTNAME = "rest.ensembl.org"

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):


    #Creating a function in order to get a dictionary with the key and value of every endpoint.
    def endpoints(self, url):
        dictionary = dict()
        if '?'in url:
            url_split1 = url.split('?')[1]
            url_split2 = url_split1.split(" ")[0]
            endpoints_list=url_split2.split("&")
            for endpoint in endpoints_list:
                try:
                    key = endpoint.split("=")[0]
                    value = endpoint.split("=")[1]
                    dictionary[key] = value
                except IndexError:
                    pass
        return dictionary


    def do_GET(self):
        codigo_respuesta=200
        res_json = False
        print ("Prueba", self.path)
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the client, depending on the resource:

        #If the resource is "/" it returns HTML main page.
        if self.path == "/":
            with open("webpage3REVISADO.html", "r") as f:
                contents = f.read()

        # If the resource is "/listSpecies", it returns a list.
        elif self.path[0:12] == "/listSpecies":

            # The dictionary of the function endpoints stored in the variable parameters.
            parameters = self.endpoints(self.path)
            print(parameters)

            # In case the user has fixed a limit:
            if 'limit' in parameters:

                # Treating possible errors just in case the limit number is not included in the length of the list.
                try:
                    # Converting the limit into integer value as it was a string.
                    limit = int(parameters['limit'])
                    print(limit)

                except:
                    limit = 0
            else:
                limit = 0


            # Establishing connection with our database server:
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request("GET", "/info/species?content-type=application/json")
            r1 = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)

            # -- Read the response's body and close
            # -- the connection
            text_json = r1.read().decode("utf-8") #String format
            conn.close()

            list = json.loads(text_json) #Json format
            print("The list is: ", list)

            # In the variable list, the list contained in the key value 'species' is stored.
            list = list['species']
            print(list)

            if limit == 0:
                # Revaluing the limit variable because now we know the length of the species list.
                limit = len(list)
            else:
                limit = limit
                print("LIIIIIIIIMIT: ", limit)


            # In case JSON OPTION has been chosen:

            if 'json' in parameters:
                res_json = True
                # Creating a list with all the names of the species of the database or until the limit number:
                contents = []
                count = 0
                for i in list:
                    specie_name = i['display_name']
                    # Every time of the loop a new species is appended to the list contents.
                    contents.append(specie_name)
                    count = count+1
                    # In order to stop adding elements to the list of species that is going to be returned.
                    if count == limit:
                        break

                print("SPECIES LIST: ", contents)
                #
                contents = json.dumps(contents)

            # If not, an html page will be returned.
            else:

                contents="""
                <html>
                <body>
                <ol>
                <h3 align=center><p style="color:#fe70f4";><u>OPTION 1: SPECIES LIST</u></p>"""

                count = 0
                for i in list:
                    contents = contents+"<li>"+i['display_name']+"</li<br>"
                    count = count+1
                    if count == limit:
                        print(count)
                        break
                    #print(count)

                contents = contents+"""</ol> 
                </body>
                </html>
                """

        #-- If the resource selected is "/karyotype":

        elif self.path[0:10] == "/karyotype":

            # In the variable parameters is returned a new dictionary in this case with the specie and maybe json option.
            parameters = self.endpoints(self.path)

            # In case the only thing written in the urls is the resource "/karyotype":
            if parameters == {}:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            # In case the user does not enter any specie:
            elif not 'specie' in parameters or parameters['specie'] == '':
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            else:

            # --Associating the specie (name) to a variable called specie.
                specie = parameters['specie']
                print(specie)

                # Establishing connection with our database server:
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/info/assembly/"+specie+"?content-type=application/json")
                r1 = conn.getresponse()

                # -- Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)

                # -- Read the response's body and close
                # -- the connection
                text_json = r1.read().decode("utf-8") #String format
                conn.close()

                response = json.loads(text_json) # Json format
                print(response)

                # IN case the specie name does not exist:
                if 'error' in response:
                    codigo_respuesta = 400
                    with open("error.html", "r") as f:
                        contents = f.read()
                else:

                    # Saving our karyotipe list by looking for the key value that returns chromosomes names of the JSON file.
                    karyotype_list = response['karyotype']

                    print("KARYOPTYPE LIST: ", karyotype_list)

                    # In case there is no information about a specie:
                    if karyotype_list == []:
                        codigo_respuesta = 400
                        with open("error.html", "r") as f:
                            contents = f.read()

                    # In case JSON option has been selected:
                    elif 'json' in parameters:
                        res_json = True
                        print(karyotype_list)
                        contents = json.dumps(karyotype_list)

                    # IF not, an HTML page with the all information is returned.
                    else:
                        contents = """
                                   <html>
                                   <body>
                                   <ul>
                                   <h3 align=center><p style="color:#f8fe70";><u>OPTION 2: SPECIE KARYOTYPE</u></p>"""
                        count = 0
                        for i in karyotype_list:
                            contents = contents + "<li>" + i + "</li<br>"

                        contents = contents + """</ul> 
                                   </body>
                                   </html>
                                   """
        # If the resource "/chromosomeLength" is selected:
        elif self.path[0:17] == "/chromosomeLength":

            # Creating a dictionary with specie and chromo endpoints and maybe json (optional):
            parameters = self.endpoints(self.path)
            print("PARAMETERS DICTIONARY: ", parameters)

            # In case the only thing written in the urls is the resource "/chromosomeLength":
            if parameters == {}:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            # In case the user does not establish a chromo and/or a specie or chromo/species not in parameters:
            elif not 'chromo' in parameters or not 'specie' in parameters or parameters['chromo'] == '' or parameters['specie'] == '':
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            else:
                chromo = parameters['chromo']
                specie = parameters['specie']
                print("Chromo; ", chromo)
                print("Specie:", specie)

                # Establishing connection with our database server:
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
                print("RESPONSE: ", response)

                # Dealing with possible errors, wrong values by the user:
                if 'error' in response:
                    codigo_respuesta = 400
                    with open("error.html", "r") as f:
                        contents = f.read()
                else:
                    # Saving in the variable 'list", a list stored in the key value 'top level region' of the json file got.
                    list = response['top_level_region']
                    print("The list of available chromosomes is :", list)

                    # Getting the length of the chromosome entered by the user:
                    length = "This chromosome does not exist for the specie selected"
                    for i in list:
                        if i['name'] == chromo:
                            length = i['length']
                    print(length)

                    #IF JSON option has been chosen:
                    if 'json' in parameters:
                        res_json = True
                        contents = json.dumps(length)

                    #IF NOT, an HTML page will be returned.
                    else:

                        contents = """
                                              <html>
                                              <body>
                                              <ul>
                                              <h3 align=center><p style="color:#adfe70";><u>OPTION 3: CHROMOSME LENGTH</u></p>"""

                        contents = contents + "<li>" + "The length of the chromosome  " + chromo +",  specie  " + specie +\
                                   ",  is: " + str(length) + "</li>"

                        contents = contents + """</ul> 
                                              </body>
                                              </html>
                                          """

        # In case resource "/geneSeq" was selected:
        elif self.path[0:8] == "/geneSeq":

            #Returning a dictionary with all the endpoints: gene and maybe json option.
            parameters = self.endpoints(self.path)
            print(parameters)

            # In case the only thing written in the urls is the resource "/geneSeq":
            if parameters == {}:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            # In case the user does not establish a specie
            elif not 'gene' in parameters or parameters['gene'] == '':
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            else:
                # Associating the gene name to a variable called 'gene':
                gene = parameters['gene']

                # Establishing connection in order to obtain gene id:
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
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
                print("RESPONSE:", response)


                # In case the gene does not exist or the user has written a wron gene name.
                if 'error' in response:
                    codigo_respuesta = 400
                    with open("error.html", "r") as f:
                        contents = f.read()

                else:
                    # Searching for the id of the gen entered by the user.
                    id = response['data'][0]['id']
                    print("ID: ", id)


                    # Establishing a new connection in order to obtain the sequence knowing the gene id:
                    conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")
                    r1 = conn.getresponse()

                    # -- Print the status
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)

                    # -- Read the response's body and close
                    # -- the connection
                    text_json = r1.read().decode("utf-8")  # String format
                    conn.close()

                    dictionary = json.loads(text_json)
                    print("DICTIONARY:", dictionary)

                    #Getting the human sequence by the key value 'seq' in the dictionary returned.
                    human_sequence = dictionary['seq']
                    print("HUMAN GENE SEQUENCE;", human_sequence)

                    # If JSON parameter is selected:
                    if 'json' in parameters:
                        res_json = True
                        contents = json.dumps(human_sequence)

                    # If not, an HTML page will be returned.
                    else:

                        contents = """
                                              <html>
                                              <body>
                                              <ul>
                                              <h3 align=center><p style="color:#fed570";><u>OPTION 4: SEQUENCE OF A HUMAN GENE</u></p>"""

                        contents = contents + "<li>" + human_sequence + "</li<br>"

                        contents = contents + """</ul> 
                                              </body>
                                              </html>
                                              """

        # In case "/geneInfo" was selected:
        elif self.path[0:9] == "/geneInfo":

            # Creating a dictionary with the key words: gene and maybe json (optional):
            parameters = self.endpoints(self.path)
            print("ENDPOINTS DICTIONARY: ", parameters)

            # In case the only thing written in the urls is the resource "/geneInfo":
            if parameters == {}:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            # In case the user does not establish a specie
            elif not 'gene' in parameters or parameters['gene'] == '':
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            else:

                # Associating gene written by the user to the variable 'gene':
                gene = parameters['gene']


                # Establishing connection to the database server in order to get the id gene:
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
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
                print("RESPONSE:",response)

                # In case the gene does not exist or the user has written a wrong gene name.
                if 'error' in response:
                    codigo_respuesta = 400
                    with open("error.html", "r") as f:
                        contents = f.read()

                else:

                    # Retrieving the id (by indexing the Json dictionary)
                    id = response['data'][0]['id']
                    print("ID",id)


                    # Establishing a new connection in order to return info about this gene: start, end, length, id and chromosome
                    conn.request("GET", "/overlap/id/" + id + "?feature=gene;content-type=application/json")
                    r1 = conn.getresponse()

                    # -- Print the status
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)

                    # -- Read the response's body and close
                    # -- the connection
                    text_json = r1.read().decode("utf-8")  # En string format
                    conn.close()

                    dictionary = json.loads(text_json)
                    print("DICTIONARY:", dictionary)

                    # Making calculations in order to return:

                    # The start and end by indexing in the dictionary:
                    start = dictionary[0]['start']
                    end = dictionary[0]['end']

                    # The length by substracting end minus start:
                    length = end-start

                    # ID by indexing:
                    id = dictionary[0]['id']

                    # Chromosome by indexing:
                    chromosome = dictionary[0]['assembly_name']

                    # In case JSON OPTION was selected:
                    if 'json' in parameters:
                        res_json = True
                        contents = {}
                        names = ["Start", "End", "Length", "Id", "Chromosome"]
                        info = [start, end, length, id, chromosome]
                        # Creating a dictionary with both lists:
                        contents = dict(zip(names, info))


                        print("CONTENTS: ",contents)

                        # Returning a json file
                        contents = json.dumps(contents)

                    # If Json option is not selected, an HTML file will be returned.
                    else:
                        contents="""
                                              <html>
                                              <body>
                                              <ul>
                                              <h3 align=center><p style="color:#70c2fe";><u>OPTION 5: INFORMATION ABOUT A HUMAN GENE</u></p>"""

                        contents = contents + " The end is: " + str(end) + "<br> The start is: "+str(start)+"<br> The lenght is: "+\
                                   str(length)+"<br> The ID is: "+str(id)+ "<br>The chromosome is: "+str(chromosome)+"<br>"""

                        contents = contents + """</ul> 
                                              </body>
                                              </html>
                                              """

        # In case resource "/geneCal" was selected:
        elif self.path[0:8] == "/geneCal":

            # A dictionary is created with all the endopoints: gene and maybe json.
            parameters = self.endpoints(self.path)
            print("ENDPOINTS DICTIONARY: ", parameters)

            # In case the only thing written in the urls is the resource "/geneCal":
            if parameters == {}:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            # In case the user does not establish a specie or gene not in parameters:
            elif not 'gene' in parameters or parameters['gene'] == '':
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            else:

                # Associating the value in the key 'gene' of the dictionary to a variable called 'gene'
                gene = parameters['gene']

                # Establishing connection with our database server in order to retrieve the ID of the gene selected by the user.
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
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
                print("RESPONSE:", response)

                # In case the gene does not exist or the user has written a wrong gene name.
                if 'error' in response:
                    codigo_respuesta = 400
                    with open("error.html", "r") as f:
                        contents = f.read()

                else:

                    # Retrieving the id (by indexing the Json dictionary)
                    id = response['data'][0]['id']
                    print("ID", id)

                    # Establishing a new connection one we know the ID to retrieve the information:
                    conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")
                    r1 = conn.getresponse()

                    # -- Print the status
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)

                    # -- Read the response's body and close
                    # -- the connection
                    text_json = r1.read().decode("utf-8")  # En string format
                    conn.close()

                    dictionary = json.loads(text_json)
                    print("DICTIONARY:", dictionary)

                    # By looking on the key value 'seq', the sequence is retrieved.
                    human_seq = dictionary['seq']
                    print("HUMAN GENE SEQUENCE;", human_seq)

                    # Creating an object and using some of its methods:
                    s1 = Seq(human_seq)
                    total_len = len(human_seq)
                    percA = s1.perc('A')
                    percT = s1.perc('T')
                    percG = s1.perc('G')
                    percC = s1.perc('C')

                    # In case the user has chosen the JSON OPTION:
                    if 'json' in parameters:
                        res_json = True
                        names_list = ["Total length", "Percentage A", "Percentage T", "Percentage G", "Percentage C" ]
                        calculations_list = [total_len, percA, percT, percG, percC]
                        # Returning a json file:
                        contents = json.dumps(dict(zip(names_list, calculations_list)))

                    # If not, an HTML web page will be returned.
                    else:
                        contents = """
                                              <html>
                                              <body>
                                              <ul>
                                              <h3 align=center><p style="color:#d970fe";><u>OPTION 6: CALCULATIONS ON A HUMAN GENE</u></p>"""

                        contents = contents + " Total length is: " + str(total_len) + "<br> The percentage of A is: "+str(percA)+"<br> The percentage of T is: "+\
                                   str(percT)+"<br> The percentage of G is: "+str(percG) + "<br>The percentage of C is: "+str(percC)+"<br>"""

                        contents = contents + """</ul> 
                                              </body>
                                              </html>
                                              """

        # In case resource "/geneList" was selected:
        elif self.path[0:9] == "/geneList":

            # Creating a dictionary with all the endopoints: chromo, start, end and maybe json option.
            parameters = self.endpoints(self.path)
            print("ENDPOINTS DICTIONARY: ", parameters)

            # In case the only thing written in the urls is the resource "/geneList":
            if parameters == {}:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()
            elif not 'chromo' in parameters or not 'start' in parameters or not 'end' in parameters:
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            # In case the user does not establish a chromo and/or a start or end:
            elif parameters['chromo'] == '' or parameters['start'] == '' or parameters['end'] == '':
                codigo_respuesta = 400
                with open("error.html", "r") as f:
                    contents = f.read()

            else:
                # Associating every value of the dictionary to a variable with the same name as the key value:
                chromo = parameters['chromo']
                start = parameters['start']
                end = parameters['end']

                print("CHROMO: ",chromo)
                print("START: ", start)
                print("END: ", end)

                # Establishing connection with our database server:
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/overlap/region/human/" +str(chromo)+ ":"+str(start)+"-"+str(end)+"?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon")
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
                print("RESPONSE:", response)

                if 'error' in response:
                    codigo_respuesta = 400
                    with open("error.html", "r") as f:
                        contents = f.read()

                # If JSON option is selected:
                elif 'json' in parameters:
                    res_json = True
                    # List that contains on each position a dictionary with 'external name', 'start' and 'end' of every element (i) (of every gene)
                    list = []
                    for i in response:
                        # In case it is a gene:
                        if i['feature_type'] == 'gene':
                            # Creating a dictionary for every i :
                            dictionary = dict ()
                            dictionary['external_name']=i['external_name']
                            dictionary['start'] = i['start']
                            dictionary['end'] = i['end']
                            list.append(dictionary)

                            print("LIST", list)
                            print("DICTIONARY", dictionary)


                    # In order to return a json file.
                    contents = json.dumps(list)

                # If not, an HTML web page will be returned.
                else:
                    contents = """
                                                      <html>
                                                      <body>
                                                      <ol>
                                                      <h3 align=center><p style="color:#70feb9";><u>OPTION 7: GENES LOCATED ON A CHROMOSOME FROM START TO END POSITIONS</u></p>"""


                    for element in response:
                        if element['feature_type'] == 'gene':
                            contents = contents+"<li>"+"GENE "+(str(element['external_name']) +";   START:"+ " " + str(element['start'])+ "   END:"+" " + str(element['end']))+"</li><br>"



                    contents = contents + """</ol> 
                                                                  </body>
                                                                  </html>
                                                                  """


        else:
            codigo_respuesta = 400
            with open("error.html", "r") as f:
                contents = f.read()

        print(self.requestline)


        # Generating the response message
        self.send_response(codigo_respuesta)  # -- Status line: OK! #El navegador va a ser contestado.

        if res_json:
            self.send_header('Content-Type', 'application/json')

        else:
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
