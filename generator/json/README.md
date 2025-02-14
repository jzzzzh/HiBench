## Run ./utils/dataset_builder.py to build the Json dataset.

# Questions and Directions

*ChildCount*: "How many subjects does Computing Dept have?"
*Direction*: How many node N2 does node N1 have.
python
def gen_anwser_child_count(scenario:str) -> str,int:
  random Node_1
  random Node_2 -> Node_1
  return question, anwser


*NodeDepth*: "Which level does the node 'Computing Dept' in?"
*Direction*: Depth of a node.
python
def gen_anwser_node_depth(scenario:str) -> str,int:
  random Node
  return question, anwser


*LevelCount*: "How many departments does a university has?" 
*Direction*: How many nodes in level x.
python
def gen_anwser_level_count(scenario:str) -> str,int
  random level_name
  return question, anwser



*NodeAttribute*: "What is the university name?"
*Direction*: What info is on leaf x.
python
def gen_anwser_node_attribute(scenario:str) -> str,int
  random Node_1
  get attribute of Node_1
  return question, anwser


*LevelNodes*: "What are the names of the departments in the university?"
*Direction*: What are the names of the nodes in level x.
python
def gen_anwser_level_nodes(scenario:str) -> str,int
  random level_name
  return question, anwser


*PathDownToUp*: "If student need to find the department, what the path he need to be taken"
*Direction*: What is the path of one node to the other node (these two nodes are in different layers)? (down to up)
python
def gen_anwser_path_down_to_up(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser


*PathUpToDown*: "If the department is coming to find the student, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the other node? (up to down)
python
def gen_anwser_path_up_to_down(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser

*SharedAncestorSameLevel*: "What is the closest shared upper-level compoent between Jason and Mike? "
*Direction*: What is the closest shared upper-level compoent between two nodes in same level.
python
def gen_anwser_shared_ancestor_same_level(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser

*SharedAncestorDiffLevel*: "What is the closest shared upper-level compoent between Jason and Department of Computing? "
*Direction*: What is the closest shared upper-level compoent between two nodes in different level.
python
def gen_anwser_shared_ancestor_diff_level(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser

*PathBetweenNodes*: "If some when wants to go to Node 1, and satrting from node 2, what is the path he need to be taken?"
*Direction*: What is the path of the one node to the other node?
python
def gen_anwser_path_between_nodes(scenario:str) -> str,int
  random Node_1
  random Node_2 -> Node_1
  return question, anwser
