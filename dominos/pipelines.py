import mysql.connector

class DominosPipeline:

    def process_item(self, item, spider):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='actowiz',
            database='dominos'
        )
        cur = conn.cursor()

        query = 'insert ignore into store_data(store,city, pin_code, address, landmark, closing_time, phone_number, website_url, map_url, page_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(query, (item['name'], item['city'], item['pincode'], item['address'], item['landmark'], item['closing_time'], item['phone'], item['website'],item['map_url'], item['page_url']))
        conn.commit()
        conn.close()