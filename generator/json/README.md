## Run ./utils/dataset_builder.py to build the Json dataset.

# Questions and Directions

*Question_1*: "How many subjects does Computing Dept have?"
*Direction*: How many node N2 does node N1 have.
python
def gen_anwser_type_1(scenario:str) -> str,int:
  random Node_1
  random Node_2 -> Node_1
  return question, anwser


*Question_2*: "Which level does the node 'Computing Dept' in?"
*Direction*: Depth of a node.
python
def gen_anwser_type_2(scenario:str) -> str,int:
  random Node
  return question, anwser


*Question_3*: "How many departments does a university has?" 
*Direction*: How many nodes in level x.
python
def gen_anwser_type_3(scenario:str) -> str,int
  random level_name
  return question, anwser


*Question_4*: "Does Dr. Peter teach Student Jason?"
*Direction*: Relationship between two nodes.
python
def gen_anwser_type_4(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser


*Question_5*: "What is the university name?"
*Direction*: What info is on leaf x.
python
def gen_anwser_type_5(scenario:str) -> str,int
  random Node_1
  get attribute of Node_1
  return question, anwser


*Question_6*: "What are the names of the departments in the university?"
*Direction*: What are the names of the nodes in level x.
python
def gen_anwser_type_6(scenario:str) -> str,int
  random level_name
  return question, anwser


*Question_7*: "If student need to find the department, what the path he need to be taken"
*Direction*: What is the path of one node to the other node (these two nodes are in different layers)? (down to up)
python
def gen_anwser_type_7(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser



*Question_8*: "If the department is coming to find the student, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the other node? (up to down)
python
def gen_anwser_type_8(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser

*Question_9*: "What is the closest shared upper-level compoent between Jason and Mike? "
*Direction*: What is the closest shared upper-level compoent between two nodes in same level.
python
def gen_anwser_type_9(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser

*Question_10*: "What is the closest shared upper-level compoent between Jason and Department of Computing? "
*Direction*: What is the closest shared upper-level compoent between two nodes in different level.
python
def gen_anwser_type_10(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser

*Question_11*: "If some when wants to go to Node 1, and satrting from node 2, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the other node?
python
def gen_anwser_type_11(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser
