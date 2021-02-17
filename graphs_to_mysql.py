import numpy as np
import matplotlib
# for writing to file, we need to use AGG backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mysql.connector
import base64

#Convert image into base64 string
def convertToBase64String(filename):
    # Convert digital data to string format
    with open(filename, 'rb') as img_file:
        encode = base64.b64encode(img_file.read())
    return encode

# function to insert graph images into database
def insert_graphs(id, image):
    connection = mysql.connector.connect(database='jinder',
                                         user='root',
                                         password='password')
    
    # list of relevant queries
    cursor = connection.cursor()
    
    sql_delete_graphs_query = """DELETE FROM user_graph"""
    sql_insert_graphs_query = """INSERT INTO user_graph
                      (graph_id, graph_code) VALUES (%s,%s)"""
    
    # call function to convert image into string
    graphCode = convertToBase64String(image)

    # Convert data into tuple format
    insert_graph_tuple = (id, graphCode)
    
    # Check if there is existing data in user_graph   
    try:
        cursor.execute(sql_insert_graphs_query, insert_graph_tuple)
        connection.commit()
    except mysql.connector.IntegrityError as err:
        if err.msg.find('Duplicate entry') != -1:
            cursor.execute(sql_delete_graphs_query)
            cursor.execute(sql_insert_graphs_query, insert_graph_tuple)
            connection.commit()

    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("graph saved into database")

def generate_graphs(sorted_df):

    # Plot pie chart by skills
    sorted_skill_list = []    
    sorted_skill_list.append(sorted_df.col.str.contains(r'java').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'javascript').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'python').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'html').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'css').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'sql').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'react').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'android').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'.net').sum())
    sorted_skill_list.append(sorted_df.col.str.contains(r'spring').sum())

    labels = ['Java','Javascript','Python','HTML5', 'CSS', 'SQL', 'React', 'Android', '.NET', 'Spring']
    sizes = np.array(sorted_skill_list)
    def whole_value(val):
        a  = np.rint(val/100*sizes.sum())
        return int(a)
    plt.pie(sorted_skill_list, labels = labels, autopct=whole_value)
    plt.axis('equal')
    plt.title("Jobs Listings Categorised By Skills")
    plt.savefig('graph1.png')      
    insert_graphs(1,'graph1.png')
    
    # clear current plot to draw new graph
    plt.clf()
    
    # Plot bar graph by job type
    sorted_type_list = []
    sorted_type_list.append(sorted_df.col.str.contains(r'programmer').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'analyst').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'developer').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'tester').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'data scientist').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'web').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'engineer').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'fullstack').sum())
    sorted_type_list.append(sorted_df.col.str.contains(r'backend').sum())
    
    x = ['Programmer', 'Analyst', 'Developer', 'Tester', 'Data Scientist', 'Web', 'Engineer', 'Fullstack', 'Backend']
    plt.barh(x, sorted_type_list)
    plt.xlabel("Number of jobs listed")
    plt.ylabel("List of Job Types")
    plt.title("Jobs Listings Categorised By Job Types")
    for index, value in enumerate(sorted_type_list):
        plt.text(value, index, str(value))
    plt.tight_layout()
    plt.savefig('graph2.png')
    insert_graphs(2, 'graph2.png')