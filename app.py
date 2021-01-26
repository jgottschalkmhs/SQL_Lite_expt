import sys
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
DATABASE
"""

# SQL CONNECTION goes here
# db_engine = create_engine('sqlite://username:password/database.db')
db_engine = create_engine('sqlite:///database.db')
db_tables = db_engine.table_names()
print('Tables', db_tables)

Session = sessionmaker(bind=db_engine)
session = Session()

"""
CLASSES
"""

# base class for all table-related classes
Base = declarative_base()

# PRODUCT CLASS goes here
# table name must match DB table name exactly!!
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    def __repr__(self):
        display_price = "{:.2f}".format(self.price)
        return f"{self.name} : ${display_price}"



"""
FUNCTIONS
"""
def list_all_products():
  print()
  print('All products:')

  # LIST ALL code goes here
  products = session.query(Product).all()

  for product in products:
      print(product)

  print()
  input('Press Enter to return to menu...')


def search_for_product():
    print()
    search_term = input('Please enter a search term: ')

    # SEARCH code goes here
    search_filter = Product.name.like('%' + search_term + '%')
    products = session.query(Product).filter(search_filter).all()

    for product in products:
        print(product)
  
    print()
    input('Press Enter to return to menu...')

def add_new_product():
  print()
  print('Add a new product:')

  # NEW PRODUCT code goes here
  new_name = input('Product Name: ')
  new_desc = input('Description: ')
  new_price= num_check('Price: ', float)
  new_stock = num_check('Stock: ', int)

  new_product = Product(
      name = new_name, 
      description = new_desc,
      price = new_price,
      stock = new_stock
  )

  session.add(new_product)
  session.commit()

  print()
  input('Press Enter to return to menu...')

def delete_product():
    print()
    print('Delete product:')

    # DELETE code goes here
    products = session.query(Product).all()

    for product in products:
        print(f"{product.id}: {product.name}")

    user_input = num_check('Enter ID of the product to delete: ', int)

    # Retrieve product to be deleted
    product = session.query(Product).filter_by(id = user_input).one()

    session.delete(product)
    session.commit()

    print()
    input('Press Enter to return to menu...')


# Other functions go here
def decorator(statement: str, decoration: str) -> None:
    print()
    print(decoration * len(statement))
    print(statement)
    print(decoration * len(statement))
    print()
    
def num_check(question, num_type):

    if num_type == float:
        error = "Please enter a number that is more than zero\n"
    else:
        error = "Please enter a whole number that is more than zero\n"

    valid = False
    while not valid:

        try:

            response = num_type(input(question))

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)

"""
MAIN MENU
"""

# Main routine goes here...

decorator('Hello! Welcome to the Cake Shop!', "*")

while True:
  print()
  print('What would you like to do?')
  print('1. List all products')
  print('2. Search for a product')
  print('3. Add a new product')
  print('4. Delete product')
  print('5. Quit')
  print()

  user_choice = input('Please enter a number: ')

  if user_choice == '1':
    list_all_products()
  elif user_choice == '2':
    search_for_product()
  elif user_choice == '3':
    add_new_product()
  elif user_choice == '4':
    delete_product()
  elif user_choice == '5':
    print()
    print('Goodbye!')

    # Exit app
    sys.exit(0)
  else:
    print()
    print('Sorry that is not a valid number')