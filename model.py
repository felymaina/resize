import sqlite3

class ImageResizerDB:
    def __init__(self, db_path='image_resizer.db'):
        self.db_path = db_path
        self.create_table()

    # Create the table if it doesn't exist
    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS ImageResizer (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            originalImage BLOB NOT NULL, 
                            size1 BLOB, 
                            size2 BLOB, 
                            size3 BLOB
                          )''')

        conn.commit()
        conn.close()

    # Insert a new image record
    def insert_image(self, original_image, size1=None, size2=None, size3=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = '''INSERT INTO ImageResizer (originalImage, size1, size2, size3) 
                   VALUES (?, ?, ?, ?)'''
        cursor.execute(query, (original_image, size1, size2, size3))

        conn.commit()
        conn.close()

    # Read an image record by ID
    def read_image_by_id(self, image_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = '''SELECT originalImage, size1, size2, size3 FROM ImageResizer WHERE ID = ?'''
        cursor.execute(query, (image_id,))
        result = cursor.fetchone()

        conn.close()
        return result  # Returns a tuple with the original and resized images

    # Update resized images for a specific ID
    def update_image(self, image_id, size1=None, size2=None, size3=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = '''UPDATE ImageResizer
                   SET size1 = ?, size2 = ?, size3 = ?
                   WHERE ID = ?'''
        cursor.execute(query, (size1, size2, size3, image_id))

        conn.commit()
        conn.close()

    # Get all image records
    def get_all_images(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = '''SELECT ID, originalImage, size1, size2, size3 FROM ImageResizer'''
        cursor.execute(query)
        results = cursor.fetchall()

        conn.close()
        return results  # Returns a list of tuples, each tuple representing an image record