from app import db, models
import re, os

"""
--Alkali Metals: 1
--Alkaline Earth Metals: 2
--Transition Metals: 3
--Poor Metals: 4
--Other Non-Metals: 5
--Halogens: 6
--Noble Gases: 7
--Actinide: 8
--Lanthanide: 9

atomic_number
group_number
"""
def main():
    for i in range(1,119):
        e = models.Element.query.get(i)
        atom_num = e.atomic_number #Collecting atomic number for each element
        col_num = e.column_number

        if col_num != 1 and atom_num != 1:
            e.group_number = 1
            db.session.add(e)
            db.session.commit()

        elif col_num == 2:
            e.group_number = 2
            db.session.add(e)
            db.session.commit()

        elif 57 <= atom_num <= 71:
            e.group_number = 8
            db.session.add(e)
            db.session.commit()

        elif 89 <= atom_num <= 103:
            e.group_number = 9
            db.session.add(e)
            db.session.commit()

        elif col_num == 17:
            e.group_number = 6
            db.session.add(e)
            db.session.commit()

        elif col_num == 18:
            e.group_number = 7
            db.session.add(e)
            db.session.commit()

        elif 4 <= col_num <= 11 or e.symbol.lower() == "sc" or e.symbol.lower() == "y":
            e.group_number = 3
            db.session.add(e)
            db.session.commit()

        elif atom_num in [13,30,31,32,48,49,50,51,80,81,82,83,84]:
            e.group_number = 4
            db.session.add(e)
            db.session.commit()

        elif atom_num in [1,5,6,7,8,9,14,15,16,17,33,34,36,52,53,85]:
            e.group_number = 5
            db.session.add(e)
            db.session.commit()

if __name__ == "__main__":
    main()