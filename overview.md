## Task Category

### Version #1
**Essential**: **_plain structure (fundamental), JSON_**  
**Practical**: **_formula, code, paper_**

### Version #2
**Essential**: **_plain structure, JSON_**  
**Intermediate**: **_formula, code_**  
**Practical**: **_paper_**

### Version #3
**Essential**: **_plain structure, JSON_**  
**Analytical**: **_formula, code_**  
**Textual**: **_paper_**

### Which category method is better? Your reason?

---

## Ability Dimensions

### **Dimension A: Relationship Awareness**  
_Finding relationships or paths in a hierarchy._
can be addressed by using partial structure information.

### **Dimension B: Structural Understanding**  
_Traversing or comparing structures, checking properties, and enumerating._
need to be addressed by using whole structure information, or cross structure.

### **Dimension C: Structural Modification**  
_Adding, removing, or transforming nodes in a hierarchical structure._


### **Dimension D: Analytical Reasoning**  
_Performing mathematical or algorithmic complexity analyses._

### **Dimension E: Textual Reasoning**  
_Reasoning about textual context and organizing paper sections._

---

## **Plain Structure (Fundamental)**
- **add_node** → **C** (_Structural Modification_)  
- **all_ancestor** → **A** (_Relationship Awareness_)  
- **all_children** → **A** (_Relationship Awareness_)  
- **common_ancestor** → **A** (_Relationship Awareness_)  
- **isomorphic** → **B** (_Structural Understanding_)  
- **remove_node** → **C** (_Structural Modification_)  
- **node_depth** → **A** (_Relationship Awareness_)  
- **leaf** → **A** (_Relationship Awareness_)  
- **root** → **A** (_Relationship Awareness_)  
- **balance** → **B** (_Structural Understanding_)  
- **prefix_traversal** → **B** (_Structural Understanding_)  
- **infix_traversal** → **B** (_Structural Understanding_)  
- **postfix_traversal** → **B** (_Structural Understanding_)  
- **traversal_order_verification** → **B** (_Structural Understanding_)  
- **mirror_tree** → **C** (_Structural Modification_)  

---

## **JSON**
- **child_count** → **A** (_Relationship Awareness_)  
- **node_depth** → **A** (_Relationship Awareness_)  
- **level_count** → **B** (_Structural Understanding_)
- **node_attribute** → **A** (_Relationship Awareness_)  
- **level_nodes** → **B** (_Structural Understanding_)  
- **path_down_to_up** → **A** (_Relationship Awareness_)  
- **path_up_to_down** → **A** (_Relationship Awareness_)  
- **shared_ancestor_same_level** → **A** (_Relationship Awareness_)  
- **shared_ancestor_diff_level** → **A** (_Relationship Awareness_)  
- **path_between_nodes** → **A** (_Relationship Awareness_)  

### Task combine:
- shared_ancestor_same_level → common ancestor
- shared_ancestor_diff_level → common ancestor

- path_down_to_up → path finding
- path_up_to_down → path finding
- path_between_nodes → path finding

### Task rename:
- level_count → level_node_count
- level_nodes → level_node_name

---

## **Formula**
- **calculate** → **D** (_Analytical Reasoning_)  
- **convert** → **D** (_Analytical Reasoning_)  
- **equivalent** → **D** (_Analytical Reasoning_)  

---

## **Code**
- **SpaceComplexity** → **D** (_Analytical Reasoning_)  
- **TimeComplexity** → **D** (_Analytical Reasoning_)  
- **CodeMissing** → **E** (_Textual Reasoning_)  

---

## **Paper**
- **contextual_qa** → **E** (_Textual Reasoning_)  
- **disordered_section** → **E** (_Textual Reasoning_)  
- **outline_extraction** → **E** (_Textual Reasoning_)  
