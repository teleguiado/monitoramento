def verificacion_caractere(caractere):
       if len(caractere) == 0 or caractere == None or '':
              return False
       else:
              return True
def verificacion_district(district):
       if not verificacion_caractere(district):
             return False
       else:
            district = int(district)
            if district < 1 or district > 6:
                  return False
            else:
                  return True
def verificatiom_password(password):
      if len(password) < 8:
            return False
      else:
            return True
def repeat_password(password ,repeat_pass):
      if repeat_pass != password:
            return "As senhas não são iguais."
def acronym_verification(acronym):
      if len(acronym) < 3:
            return False
      else:
            return True

def validation_login(username, password):
      if not verificacion_caractere(username):
            message = 'O login não poder ficar vazio.'
            return message
      if not verificacion_caractere(password):
            message = 'A senha nao pode ficar em branco.'
            return message
      if not verificatiom_password(password):
            message = 'A senha deve conter no minimo 8 digitos.'

def validation(name_unit, other_name, address, district, director, loc, ip, acronym):
        if not verificacion_caractere(name_unit):
            return "O campo Nome da unidade não pode ficar vazio."
        if not verificacion_caractere(other_name):
            return "O campo apelido não pode ficar vazio."
        if not verificacion_caractere(address):
              return "O campo de endereço não pode ficar vazio."
        if not verificacion_district(district):
              return "O distrito deve ser entre 1 e 6 e não pode ficar em branco."
        if not verificacion_caractere(director):
              return "O campo diretor não pode ficar vazio."
        if not verificacion_caractere(loc):
              return "O campo localização não pode ficar vazio."
        if not verificacion_caractere(ip):
              return "O campo de IP ou HOST não pode ficar vazio"
        if not verificacion_caractere(acronym) or not acronym_verification(acronym):
              return "A SIGLA não pode ficar em branco e não pode ser menor que 3 CARACTERES"