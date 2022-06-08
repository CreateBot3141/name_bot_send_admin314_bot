
def print_message_menu (namebot,user_id,id_sql,start_sql,step_sql,message_id,operation):
    import iz_func
    import iz_telegram
    db,cursor = iz_func.connect ()
    parameter01 = "name"
    parameter02 = ""
    parameter03 = ""
    parameter04 = ""
    parameter05 = ""
    name_table  = "bot_product" 
    step_sql    = step_sql 
    start_sql   = start_sql
    message_out,menu = iz_telegram.get_message (user_id,'Список продуктов',namebot)
    sign        = ['status',['start',iz_telegram.get_namekey (user_id,namebot,'Хорошо')],['stop',iz_telegram.get_namekey (user_id,namebot,'Плохо')]]
    pattern,menu = iz_telegram.get_message (user_id,'Шаблон кнопки список продуктов',namebot)
    if id_sql == 0:
        name_sql = "select id,status"
        if parameter01 != "":
            name_sql =  name_sql + ",`"+str(parameter01)+"`"
        if parameter02 != "":
            name_sql =  name_sql + ",`"+str(parameter02)+"`"
        if parameter03 != "":
            name_sql =  name_sql + ",`"+str(parameter03)+"`"
        name_sql =  name_sql + "from "+str(name_table)+" "
        name_sql =  name_sql + ' where namebot = "'+str(namebot)+'" limit %%start_list%%,%%step_list%%'

        print ('[+] name_sql:',name_sql)

        id_sql = iz_telegram.new_list(name_sql,start_sql,step_sql)


        message_id = 0
    if operation == 'new':
        sql = iz_telegram.get_list (id_sql,'new','')

    if  operation == 'reset':
        sql = iz_telegram.get_list (id_sql,'reset','')

    if  operation == 'next':
        sql = iz_telegram.get_list (id_sql,'next','')

    if  operation == 'last':
        sql = iz_telegram.get_list (id_sql,'last','')

    print ('sql',sql)

    cursor.execute(sql)
    data = cursor.fetchall()
    markup = iz_telegram.button_body_design_01 (data,pattern,parameter01,parameter02,parameter03,parameter04,parameter05,sign,id_sql)
    iz_telegram.button_end_design_01 (user_id,namebot,markup,id_sql)
    answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)


def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import iz_func
    import iz_game
    import iz_main
    import time
    import iz_telegram


    if message_in == 'Вывести список задач':
        print_message_menu (namebot,user_id,0,0,10,message_id,'new')




    if message_in == 'Включить':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Система включена','S',message_id)  

        user_id  = '590719271'
        variable = 'Статус бота'
        namebot  = '@send314_bot'
    
        #iz_telegram.save_variable (user_id,namebot,"Статус бота",'ON')
        iz_func.save_variable (user_id,"Статус бота",'ON',namebot)
        status = ""        
   
    if message_in == 'Выключить':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Система выключена','S',message_id)

        user_id  = '590719271'
        variable = 'Статус бота'
        namebot  = '@send314_bot'
    
        #iz_telegram.save_variable (user_id,namebot,"Статус бота",'ON')
        iz_func.save_variable (user_id,"Статус бота",'OFF',namebot)


        #iz_telegram.save_variable (user_id,namebot,"Статус бота",'OFF')
        status = ""

    if message_in == 'TEST':
        answer = iz_telegram.save_tovar (user_id,namebot,"TEST",'1','2','3')

    if message_in.find ('TEST') != -1:                    
        status_bota =  iz_func.load_variable (user_id,"Статус бота",namebot)
        message_send = iz_func.send_message (user_id,status_bota,'S',namebot)

    if message_in == '/add_user_grup':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Введите новый каталог для чтения','S',message_id)
        iz_telegram.save_variable (user_id,namebot,"status",'Ввод каталога')

    if status == 'Ввод каталога':
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Информация записана','S',message_id)
        iz_telegram.save_variable (user_id,namebot,"status",'')
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO send314_bot_catalog_read (name,status,user_id) VALUES ('{}','','{}')".format (message_in,user_id)
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid        

    if message_in == '/list_user_grup':
        #message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Список рабочик каталог','S',message_id)
        #iz_telegram.save_variable (user_id,namebot,"status",'Ввод каталога')
        db,cursor = iz_func.connect ()
        message_out,menu = iz_telegram.get_message (user_id,'Список рабочик каталог',namebot)
        message_out = message_out + '\n\n\n'
        #message_out = message_out.replace('%%Процент%%',str(minmin))   
        #message_out = message_out.replace('%%Заявка%%',str(command))
        markup = ''

        sql = "select id,name from send314_bot_catalog_read where 1=1;".format(namebot)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,name = rec.values() 
            message_out = message_out + name + '\n'


        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)        

    if message_in.find ('info') != -1:
        import json
        json_string  = iz_func.change_back(message_in.replace('info_',''))
        data_json = json.loads(json_string)
        operation = data_json['o']

        if operation == 'key':
            id_sql   = data_json['id']
            list_sql = data_json['sql']
            iz_telegram.replacement ('bot_product','status',id_sql,['start','stop'])
            print_message_menu (namebot,user_id,list_sql,0,10,message_id,'reset')

