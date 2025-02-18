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

### **Dimension A: Structural Modification**  
_Adding, removing, or transforming nodes in a hierarchical structure._

### **Dimension B: Relationship Awareness**  
_Finding relationships or paths in a hierarchy._
can be addressed by using partial structure information.

### **Dimension C: Structural Understanding**  
_Traversing or comparing structures, checking properties, and enumerating._
need to be addressed by using whole structure information, or cross structure.

### **Dimension D: Analytical Reasoning**  
_Performing mathematical or algorithmic complexity analyses._

### **Dimension E: Textual Reasoning**  
_Reasoning about textual context and organizing paper sections._

---

## **Plain Structure (Fundamental)**
- **add_node** → **A** (_Structural Modification_)  
- **all_ancestor** → **B** (_Relationship Awareness_)  
- **all_children** → **B** (_Relationship Awareness_)  
- **common_ancestor** → **B** (_Relationship Awareness_)  
- **isomorphic** → **C** (_Structural Understanding_)  
- **remove_node** → **A** (_Structural Modification_)  
- **node_depth** → **B** (_Relationship Awareness_)  
- **leaf** → **B** (_Relationship Awareness_)  
- **root** → **B** (_Relationship Awareness_)  
- **balance** → **C** (_Structural Understanding_)  
- **prefix_traversal** → **C** (_Structural Understanding_)  
- **infix_traversal** → **C** (_Structural Understanding_)  
- **postfix_traversal** → **C** (_Structural Understanding_)  
- **traversal_order_verification** → **C** (_Structural Understanding_)  
- **mirror_tree** → **A** (_Structural Modification_)  

---

## **JSON**
- **child_count** → **B** (_Relationship Awareness_)  
- **node_depth** → **B** (_Relationship Awareness_)  
- **level_count** → **C** (_Structural Understanding_)
- **node_attribute** → **B** (_Relationship Awareness_)  
- **level_nodes** → **C** (_Structural Understanding_)  
- **path_down_to_up** → **B** (_Relationship Awareness_)  
- **path_up_to_down** → **B** (_Relationship Awareness_)  
- **shared_ancestor_same_level** → **B** (_Relationship Awareness_)  
- **shared_ancestor_diff_level** → **B** (_Relationship Awareness_)  
- **path_between_nodes** → **B** (_Relationship Awareness_)  

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
