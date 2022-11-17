from app import app

if __name__=='__main__':
    # print('Banana: STARTING')

    app.run(port=5000, use_reloader=False)
    
    # print('Banana: STOPPED')