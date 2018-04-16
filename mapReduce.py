'''
MapReduce
'''

from pyactor.context import set_context, create_host, sleep, shutdown, Host
import time, sys, os
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++ Maper: Encarregada de rebre informacio, +++++
#++++++++++ formatarla i almacenar-la		    +++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Mapper(object):
    _tell = ['start', 'setr', 'fmap']
    _ask = []
    _ref = ['setr']

    #Start inicialitza les variables i acumuladors requerits pel maper
    def start(self, fitxer, tipus):
	self.num=0
	self.out = {}
	f = open(fitxer, "r")
	if tipus == "w":	
		for line in f:		
			for i in line.replace(".",'').replace(",",'').replace("!",'').replace("?",'').replace(":",'').replace(";",'').replace('"','').replace("'",'').replace("(",'').replace(")",'').split():
				self.fmap(self.num, i)
			self.num = self.num + 1
	else:
		for line in f:		
			for i in line.split():
				self.fmap(self.num, "paraula")
			self.num = self.num + 1

	self.reducer.recive(self.out)

    #fMap encarregada de almacenar les paraules amb les degudes repeticions
    def fmap(self, k, v):
	if self.out.has_key(v):
		self.out[v] = self.out[v] + 1
	else:
		self.out[v] = 1

    #Guardem el reducer per cridarlo despres
    def setr (self, reducer):
	self.reducer= reducer

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++ Reducer: Encarregada de rebre parametres, +++++
#++++++++++ reduir-los i almacenarlos   	      +++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Reducer(object):
    _tell = ['start', 'recive', 'doReduce', 'reduce']
    _ask = []

    #Start inicialitza les variables i acumuladors requerits pel reducer
    def start(self, numero):
	self.nDic = numero
	self.out = {}
	self.diccionaris = []
	self.inici = time.time()
	
    #Recupera les claus del acumulador i les almacena utilitzant la comanda reduce

    def doReduce(self):
	for key in self.out.keys():
		self.reduce(key, self.out[key])

	print "El total de temps es: "+str(time.time()-self.inici)
	print "\nPrem enter per acabar"

    #Reduce rep per parametre una clau i la seva respectiva llista de valors, sumant tots els valors dels que disposa i almacenant el resultat
    def reduce(self, k, v):

	print "Valors: "+str(sum(self.out[k]))+"\tParaula: "+k

    #Recive sera cridada per fmap per tal de almacenar els diccionaris resultants de l'execucio, portant el compte de els diccionaris almacenats, al arribar al nombre maxim, cridara el do reducer
    def recive (self, dic):

	for paraula in  dic.keys():
		self.out.setdefault(paraula, list())
		self.out[paraula].append(dic[paraula])

	self.nDic = self.nDic - 1

	if self.nDic == 0:

		self.doReduce()

class Registry(object):
    _ask = ['get_all', 'bind', 'lookup', 'unbind']
    _async = []
    _ref = ['get_all', 'bind', 'lookup']

    def __init__(self):
        self.actors = {}

    def bind(self, name, actor):
        print "Servidor registrat amb nom: ", name
        self.actors[name] = actor

    def unbind(self, name):
        if name in self.actors.keys():
            del self.actors[name]
        else:
            raise NotFound()

    def lookup(self, name):
        if name in self.actors:
            return self.actors[name]
        else:
            return None

    def get_all(self):
        return self.actors.values()
if __name__ == "__main__":
    set_context()

    hr = create_host("http://127.0.0.1:7777/")
    reducer = hr.spawn('Red', "mapReduce/Reducer")
   
    registry = hr.spawn('regis', Registry)

    for x in range(0, int(sys.argv[1])):
	os.system("nohup python spawn.py %s mapReduce &"%str(x))
    sleep(2)

    reducer.start(int(sys.argv[1]))
    x=0
    vHost={}
    vMap={}
    for actor in registry.get_all():
	vHost[x]=actor
	vMap[x]= vHost[x].spawn('Map%s'%str(x),"mapReduce/Mapper")
	vMap[x].setr(reducer)
	x+=1

    f = open(sys.argv[2], "r")
    x=0
    tipus = sys.argv[3]
    for line in f:
	vMap[x].start(line.replace("\n", ""), tipus)
	x=x+1
    if sys.argv[3] == "w":
	print"\n\nWordCount en funcionament"
    else:
	print"\n\nCountWords en funcionament"
    raw_input("\nPrem Enter per interrompre la execucio\n")

    shutdown()
