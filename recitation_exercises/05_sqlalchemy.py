# activate venv then run via python -m flask --app 05_sqlalchemy.py run
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Column, ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# feature we don't need that is being deprecated upstream by sqlaclchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


'''
Consider the following schema:
	Forest(forest_no, forest_name, area)
	State(state_name, area)
	Coverage(entry_no, forest_no, state_name, area)

Notice how a forest can span two states
'''
'''
(1) create the tables/models, make sure you set the primary and 
    foreign keys. Look at the '05_db.txt' file to find out
    what the types of each column should be. I only used either
    an integer and a string
'''
class Forest(db.Model):
    __tablename__ = "forest_table"
    forest_no: Mapped[int] = mapped_column(primary_key=True)
    forest_name: Mapped[str]
    area: Mapped[int]
    states: Mapped[list["Coverage"]] = relationship(back_populates="forest")

    def __init__(self, forest_no, forest_name, area):
        self.forest_no = forest_no
        self.forest_name = forest_name
        self.area = area
    
class State(db.Model):
    __tablename__ = "state_table"
    state_name: Mapped[str] = mapped_column(primary_key=True)
    area: Mapped[int] 
    forests: Mapped[list["Coverage"]] = relationship(back_populates="state")

    def __init__(self, state_name, area):
        self.state_name = state_name
        self.area = area
    
class Coverage(db.Model):
    __tablename__ = "coverage_table"
    entry_no: Mapped[int] 
    forest_no: Mapped[int] = mapped_column(ForeignKey("forest_table.forest_no"), primary_key=True)
    state_name: Mapped[str] = mapped_column(ForeignKey("state_table.state_name"), primary_key=True)
    area: Mapped[int]

    forest: Mapped["Forest"] = relationship(back_populates="states")
    state: Mapped["State"] = relationship(back_populates="forests")

    def __init__(self, entry_no, forest_no, state_name, area):
        self.entry_no = entry_no
        self.forest_no = forest_no
        self.state_name = state_name
        self.area = area
    

'''
(2) populate the tables you created above, you can find the data for 
	the tables in the '05_db.txt' file. The delimiter for an entry/record 
	is ',' and for the tables it is an empty line ('\n'). Remeber to 
	drop all any previosuly created tables to avoid nay problems
'''
with app.app_context():
    db.drop_all()
    db.create_all()

    with open("05_db.txt", "r", encoding="utf-8") as file:
        lines = file.readlines() 
        
    table_num = 0
    x = 0
    for line in lines:
        print("line " + str(x) + " " + line)
        if line.strip() == "":
            table_num += 1
            continue
        x+=1

        
        split_arr = line.strip().split(',')

        if table_num == 0:
            db.session.add(Forest(int(split_arr[0]), split_arr[1], int(split_arr[2])))
        elif table_num == 1:
            db.session.add(State(split_arr[0], int(split_arr[1])))
        elif table_num == 2:
            db.session.add(Coverage(int(split_arr[0]), int(split_arr[1]), split_arr[2], int(split_arr[3])))
    
    print("Done adding entries")
    db.session.commit()
    print("Done committing")

    #3 find and print the forest name(s) with the largest area (hint: use the func.max)
    largestArea = db.session.query(func.max(Forest.area)).scalar()
    largestForestName = db.session.query(Forest.forest_name).filter(Forest.area==largestArea).first()
    print("Query Step 3: " + largestForestName[0]) 

    #(4) find and print names of all forests that are located in PA (hint: might have to join 2 tables)
    #need check coverage. every time pa listed, get the forest number
    forestNumbersInPA = db.session.query(Coverage.forest_no).filter(Coverage.state_name=="PA")
    namesOfForestsInPA = db.session.query(Forest.forest_name).filter(Forest.forest_no.in_(forestNumbersInPA)).all()
    print("Query Step 4: ", [name[0] for name in namesOfForestsInPA])
    
    # (5) find and print the number of forests for each state in descending order (hint: use func.count)
    forestsInEachState = db.session.query(Coverage.state_name, func.count(Coverage.forest_no)).group_by(Coverage.state_name).all()
    print("(not sorted) Query Step 5: ", [""+ str(entry[0]) +" "+ str(entry[1]) for entry in forestsInEachState])

    # (6) find and print the percentage of area covered by forests in all states (hint: use func.sum)
    joinedTab = db.session.query(Coverage).join(State.state_name)
    forestAreaInStates = db.session.query(Coverage.state_name, func.round(100* 
        (func.sum(Coverage.area)/State.area) )+"%").join(
        State, Coverage.state_name==State.state_name).group_by(Coverage.state_name)
    print("Query Step 6: ")
    print(forestAreaInStates.all())