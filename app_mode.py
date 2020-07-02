def get_app_mode(file_name):
    return str(file_name.split('/')[-2])


def is_prodaction(file_name):
    return str(file_name.split('/')[-2]) == 'prodaction'


def is_test(file_name):
    return str(file_name.split('/')[-2]) == 'test'