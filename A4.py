import ply.lex as lex
import ply.yacc as yacc
import time
import json
import hashlib
from typing import List, Dict, Any, Tuple

# BEGIN LEXICAL ANALYZER DEFINITION

tokens = ['BLOCK','ADD','PRINT','VIEW',
          'RUN','MINE','EXPORT','STR','INT',
          'LONG','FLOAT','LIST','TUPLE','DICT',
          'ID','STRING','NUMBER','ASSIGN','TYPEASSIGN',
          'SEPARATOR','LPAREN','RPAREN']

# Dictionary that maps the keyword string to their corresponding token
keywords = {'block':'BLOCK','add':'ADD','print':'PRINT',
            'view':'VIEW','run':'RUN','mine':'MINE',
            'export':'EXPORT','str':'STR','int':'INT',
            'long':'LONG','float':'FLOAT','List':'LIST',
            'Tuple':'TUPLE','Dict':'DICT'}

# Ignore
t_ignore = ' \t\r'           

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'//[^\n]*'
    pass

# Token matching rules are written as regexs
t_SEPARATOR = r','
t_ASSIGN = r'='
t_TYPEASSIGN = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    # Check if it's a keyword, otherwise stays 'ID'
    t.type = keywords.get(t.value, 'ID') 
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'(\d+\.\d+) | (\.\d+) | (\d+)'

    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Handle errors and specifies in which row
def t_error(t):
    print(f'Illegal character {t.value[0]!r} in row {t.lexer.lineno}')
    t.lexer.skip(1)

# END LEXICAL ANALYZER DEFINITION

#################################

# BEGIN SYNTAX ANALYSIS DEFINITION

def p_start(p):
   'start : block_definition block_operations'
   p[0]= (p[1],p[2])

def p_block_definition(p):
   'block_definition : BLOCK ID ASSIGN LPAREN attributes RPAREN'
   p[0] = ('block', p[2], p[5])

def p_block_operations(p):
   '''block_operations : block_operation
                       | block_operations block_operation'''
   if len(p) == 2: p[0] = [p[1]]
   else: p[0] = p[1] + [p[2]]   

def p_block_operation(p):
   '''block_operation : ADD ID ASSIGN LPAREN new_atts RPAREN
                      | PRINT ID 
                      | RUN ID
                      | MINE ID
                      | EXPORT ID
                      | VIEW ID'''
   if p[1] == "add":
      block_name = p[2]
      p[0] = ("AddOp", block_name, p[5])

   elif p[1] == "print":
      block_name = p[2]
      p[0] = ("PrintOp", block_name)

   elif p[1] == "run":
      block_name = p[2]
      p[0] = ("RunOp", block_name)

   elif p[1] == "export":
      block_name = p[2]
      p[0] = ("ExportOp", block_name)

   elif p[1] == "view":
      block_name = p[2]
      p[0] = ("ViewOp", block_name)

   elif p[1] == "mine":
      block_name = p[2]
      p[0] = ("MineOp", block_name)

def p_type(p):
   '''type : STR
           | INT
           | LONG
           | FLOAT
           | LIST
           | TUPLE
           | DICT'''
   p[0] = p[1]

def p_attribute(p):
   'attribute : ID TYPEASSIGN type'
   p[0] = (p[1], p[3])

def p_attributes(p):
   '''attributes : attribute 
                 | attributes SEPARATOR attribute'''
   if len(p) == 4:
      p[0] = p[1] + [p[3]]
   else:
      p[0] = [p[1]]

def p_new_att(p):
   '''new_att : ID TYPEASSIGN STRING
              | ID TYPEASSIGN NUMBER'''
   p[0] = (p[1], p[3])

def p_new_atts(p):
   '''new_atts : new_att
               | new_atts SEPARATOR new_att'''
   if len(p) == 4:
      p[0] = p[1]+[p[3]]
   else:
      p[0] = [p[1]]

def p_error(p):
    if p is None:
        print("Syntax error at EOF")
    else:
        print(f"Syntax error at {p.value!r} (line {p.lineno})")

   
# END SYNTAX ANALYSIS DEFINITION

# BLOCKCHAIN CLASS
class Blockchain:
    def __init__(self, block_name: str, schema: Dict[str, str]):
        self.name = block_name
        self.schema = schema # Stores the attribute types (e.g., {'client': 'STR', 'value': 'INT'})
        self.chain: List[Dict[str, Any]] = []
        self.current_data: List[Dict[str, Any]] = []
        
        # Create block
        self.new_block(proof='1', previous_hash='1')
        print(f" Initialized Blockchain '{self.name}' and created Block.")

    def hash(self, block: Dict[str, Any]) -> str:
        """Creates a SHA-256 hash of a block."""
        # We ensure the Dictionary is ordered to avoid inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_block(self, proof: str, previous_hash: str = None) -> Dict[str, Any]:
        """
        Creates a new Block and adds it to the chain.
        (Based on the example provided)
        """
        block = {
            'index': len(self.chain)+1,
            'timestamp': time.time(),
            'data': self.current_data,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        
        # Reset the current list of transactions/data
        self.current_data = [] 
        self.chain.append(block)
        return block

    def add(self, data: Dict[str, Any]) -> None:
        """Adds new data to the list of unmined data."""
        self.current_data.append(data)

    def mine(self) -> Dict[str, Any]:
        """Finds the proof and creates a new block, chaining it."""
        # Simple proof-of-work placeholder
        proof = "simple_proof_" + str(time.time()) 
        last_hash = self.hash(self.chain[-1])
        
        # Create a new block, which chains the blocks
        new_block = self.new_block(proof, last_hash)
        return new_block
    
    def print(self):
        """Makes the blockchain visible on the screen"""
        print(f"\n--- BLOCKCHAIN: {self.name} ({len(self.chain)} Blocks) ---")
        for block in self.chain:
            print(json.dumps(block, indent=4))

    def export(self, filename: str):
        """Creates a JSON file with the data"""
        with open(filename, 'w') as f:
            json.dump(self.chain, f, indent=4)
        print(f" Exported blockchain '{self.name}' to {filename}.")
        
    def run(self):
        """Hosts the blockchain on the computer"""
        # Placeholder for starting a simple web server
        print(f" Hosting blockchain '{self.name}' (Placeholder)")

# Key: Block ID (str)
# Value: Blockchain object
BLOCKCHAINS: Dict[str, Blockchain] = {} 

def get_py_type(type_str):
    """Maps the language type string (e.g., 'int') to a Python type object."""
    if type_str == 'int': return int
    if type_str == 'str': return str
    if type_str == 'float': return float
    return str 

def do_block_definition(block_name: str, schema_list: List[Tuple[str, str]]):
    """Implements semantics for the BLOCK instruction"""
    if block_name in BLOCKCHAINS:
        print(f"Error: Block '{block_name}' already defined.")
        return
    
    # Convert list of tuples to a dictionary for easy schema lookup
    schema = dict(schema_list)

    # Creates the block and stores the object
    BLOCKCHAINS[block_name] = Blockchain(block_name, schema)


def do_add_operation(block_name: str, data_list: List[Tuple[str, Any]]):
    """Implements semantics for the ADD instruction, reports all semantic errors found."""
    
    if block_name not in BLOCKCHAINS:
        print(f"Error: Block '{block_name}' is not defined.")
        return

    blockchain = BLOCKCHAINS[block_name]
    new_data = {}
    is_valid_transaction = True

    # Verify data types and schema
    for key, value in data_list:
        
        # Check for Unknown Attribute
        if key not in blockchain.schema:
            print(f" Semantic Error: Attribute '{key}' not in schema for '{block_name}'.")
            is_valid_transaction = False
            continue 

        expected_type_str = blockchain.schema[key]
        expected_type_py = get_py_type(expected_type_str)

        # Check for Type Mismatch
        if not isinstance(value, expected_type_py):
            print(f" Semantic Error: '{key}' expected {expected_type_str}, got {type(value).__name__}.")
            is_valid_transaction = False

        new_data[key] = value 
    
    # Store the data 
    if is_valid_transaction:
        blockchain.add(new_data)
        print(f" Added Data to '{block_name}' (Pending Mining).")
    else:
        print(f" Transaction on '{block_name}' rejected due to semantic error.")
    

def do_mine_operation(block_name: str):
    """Implements semantics for the MINE instruction."""
    if block_name not in BLOCKCHAINS:
        print(f"Error: Block '{block_name}' is not defined.")
        return
        
    blockchain = BLOCKCHAINS[block_name]
    new_block = blockchain.mine()
    print(f" Block '{new_block['index']}' mined and chained in '{block_name}'.")


def do_print_operation(block_name: str):
    """Implements semantics for the PRINT instruction."""
    if block_name not in BLOCKCHAINS:
        print(f"Error: Block '{block_name}' is not defined.")
        return

    BLOCKCHAINS[block_name].print()


def do_export_operation(block_name: str):
    """Implements semantics for the EXPORT instruction."""
    if block_name not in BLOCKCHAINS:
        print(f"Error: Block '{block_name}' is not defined.")
        return
    
    filename = f"{block_name}_blockchain.json"
    BLOCKCHAINS[block_name].export(filename)


def do_run_operation(block_name: str):
    """Implements semantics for the RUN instruction."""
    if block_name not in BLOCKCHAINS:
        print(f"Error: Block '{block_name}' is not defined.")
        return
    
    BLOCKCHAINS[block_name].run()


# Main Execution Dispatcher

def execute_program(ast: Tuple):
    """
    The main execution engine.
    Receives the AST and dispatches execution to semantic functions.
    """
    
    global BLOCKCHAINS
    BLOCKCHAINS = {} # Reset state for a clean run

    if ast is None:
        print("\nExecution terminated due to Syntax Error.")
        return
    
    # AST structure: (block_definition_tuple, list_of_operation_tuples)
    
    # Process the Block Definition
    block_def_tuple = ast[0]
    block_name = block_def_tuple[1]
    schema_list = block_def_tuple[2]
    
    print("\n---> Executing Block Definition")
    do_block_definition(block_name, schema_list)
    
    # Process all Block Operations
    block_operations_list = ast[1]
    for op_tuple in block_operations_list:
        op_type = op_tuple[0] # e.g., 'AddOp', 'MineOp'
        block_name = op_tuple[1]
        
        print(f"\n---> Executing {op_type} on {block_name}")
        
        if op_type == "AddOp":
            do_add_operation(block_name, op_tuple[2])
        elif op_type == "MineOp":
            do_mine_operation(block_name)
        elif op_type == "PrintOp":
            do_print_operation(block_name)
        elif op_type == "ExportOp":
            do_export_operation(block_name)
        elif op_type == "RunOp":
            do_run_operation(block_name)
        elif op_type == "ViewOp": 
            # VIEWOp semantics typically align with PRINT/display
            do_print_operation(block_name)

################
## CALL PARSER
################

def main():
    print("Initiating Tests")
    lexer = lex.lex()
    parser = yacc.yacc()

    # Read the file
    try:
        with open("Program_Test.txt", "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: 'Program_Test.txt' not found. Cannot run parser tests.")
        return

    curTest = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('//'):
            if curTest:
                code = "\n".join(curTest)
                print("\n Running the Tests")
                print(code)

                try:
                    # 1. Capture the AST from the parser
                    ast = parser.parse(code, lexer=lexer)
                    
                    # 2. Execute the AST to run semantics
                    if ast is not None:
                        execute_program(ast)

                except Exception as e:
                    print(f"Parser or Execution Error: {e}")
                curTest = []  # Cleaning/reset the list
            print("\n" + line)

        else:
            curTest.append(line)
            
    # Run the final test case if it exists
    if curTest:
        code = "\n".join(curTest)
        print("\n Running the Test")
        print(code)

        try:
            ast = parser.parse(code, lexer=lexer)
            
            # Execute the AST to run semantics
            if ast is not None:
                execute_program(ast)

        except Exception as e:
            print(f"Parser or Execution Error: {e}")


    print("Finalizing Tests")


if __name__ == '__main__':
    main()