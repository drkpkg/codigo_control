# -*- encoding: utf-8 -*-
import base64
import cStringIO
import qrcode

class ImpuestosInternosHelper():

    def obtenerbase64(self, numero):
        """Toma como parametro un numero y retorna una palabra en BASE64"""
        diccionario = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
                       "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b",
                       "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                       "v", "w", "x", "y", "z", "+", "/"]
        cociente = 1.0
        resto = 0
        palabra = ""
        while cociente > 0:
            cociente = numero / 64
            resto = numero % 64
            palabra = diccionario[resto] + palabra
            numero = cociente
        return palabra

    def inviertecadena(self, cadena):
        """Invierte una cadena :v"""
        return cadena[::-1]

    def obtenerverhoeff(self, cifra):
        """Genera por medio una cifra una cifra verhoeff"""
        mul = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
               [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
               [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
               [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
               [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
               [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
               [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
               [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
               [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
        per = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
               [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
               [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
               [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
               [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
               [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
               [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]
        inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
        check = 0
        numeroinvertido = self.inviertecadena(str(cifra))

        for i in range(0, len(numeroinvertido)):
            pf = ((i + 1) % 8)
            pc = int(numeroinvertido[i])
            mf = check
            mc = per[pf][pc]
            check = mul[mf][mc]
        return str(inv[check])

    def allegedrc4(self, mensaje, key):
        """Genera el cifrado Alleged Rc4 por medio de un mensaje y una llave"""
        state = []
        x = 0
        y = 0
        index1 = 0
        index2 = 0
        mensaje_cifrado = ""

        for position in range(0,256):
            state.append(position)

        for position in range(0, 256):
            index2 = (ord(key[index1]) + state[position] + index2) % 256
            state[position], state[index2] = state[index2],state[position]
            index1 = (index1 + 1) % len(key)

        for position in range(0,len(mensaje)):
            x = (x+1) % 256
            y = (state[x] + y) % 256
            state[x], state[y] = state[y], state[x]
            nuevo_mensaje = (ord(mensaje[position]) ^ (state[(state[x] + state[y]) % 256]))
            mensaje_cifrado = mensaje_cifrado + "-" + self.rellenaCero(hex(nuevo_mensaje))

        return mensaje_cifrado[1:len(mensaje_cifrado)]

    def rellenaCero(self, mensaje):
        """Rellena una cadena de cero en caso de que solo tenga longitud 1"""
        mensaje = str(mensaje).split('x')[1].upper()
        if len(mensaje) == 1:
            return "0" + mensaje
        return mensaje

    def generar_verhoeff_n_veces(self, cifra, n=2):
        """Llama a verhoeff una n cantidad de veces, por defecto son 2 iteraciones"""
        for i in range(n):
            cifra = cifra + '' + self.obtenerverhoeff(cifra)
        return str(cifra)

    def generar_codigo_control(self, numero_autorizacion, numero_de_factura, nit_ci, fecha_transaccion, monto_total, llave_dosificacion):
        """Genera un codigo de control valido para Impuestos internos"""
        verhoeff_numero_de_factura = self.generar_verhoeff_n_veces(numero_de_factura)
        verhoeff_nit_ci = self.generar_verhoeff_n_veces(nit_ci)
        verhoeff_fecha_trasaccion = self.generar_verhoeff_n_veces(fecha_transaccion.replace('/',''))
        verhoeff_monto_total = self.generar_verhoeff_n_veces(str(int(round(float(monto_total)))))

        suma_verhoeff = int(verhoeff_numero_de_factura) + int(verhoeff_nit_ci) + int(verhoeff_fecha_trasaccion) + int(verhoeff_monto_total)
        digito_verhoeff = str(self.generar_verhoeff_n_veces(str(suma_verhoeff), 5))[-5:]
        cifra_verhoeff =  self.tratar_verhoeff(digito_verhoeff)
        cadena_array_verhoeff = self.tratar_dosificacion(llave_dosificacion, cifra_verhoeff)
        cadena_concatenada = self.generar_verhoeff_concatenado(
            [numero_autorizacion, verhoeff_numero_de_factura, verhoeff_nit_ci,verhoeff_fecha_trasaccion, verhoeff_monto_total],
            cadena_array_verhoeff)
        dosificacion_verhoeff = llave_dosificacion + digito_verhoeff
        cifra_alleged4rc = self.allegedrc4(cadena_concatenada, dosificacion_verhoeff).replace('-', '')
        # ARRAYS EMPIEZAN EN CERO!!!
        suma_total_alleged = self.suma_ascii(cifra_alleged4rc)
        suma_1_alleged = self.suma_ascii(cifra_alleged4rc, 0, 5)
        suma_2_alleged = self.suma_ascii(cifra_alleged4rc, 1, 5)
        suma_3_alleged = self.suma_ascii(cifra_alleged4rc, 2, 5)
        suma_4_alleged = self.suma_ascii(cifra_alleged4rc, 3, 5)
        suma_5_alleged = self.suma_ascii(cifra_alleged4rc, 4, 5)

        alleged_tratado = self.tratar_alleged(suma_total_alleged,
                                  [suma_1_alleged, suma_2_alleged, suma_3_alleged, suma_4_alleged, suma_5_alleged],
                                  cifra_verhoeff)
        mensaje_alleged = self.obtenerbase64(alleged_tratado)
        codigo_control = self.allegedrc4(mensaje_alleged, dosificacion_verhoeff)
        return codigo_control

    def tratar_alleged(self,total_alleged, alleged_data, verhoeff_data):
        """Retorna una suma total del cifrado alleged y verhoeff"""
        suma = 0
        for position in range(len(alleged_data)):
            resultado = round(total_alleged * alleged_data[position] / verhoeff_data[position])
            suma += resultado
        return int(suma)

    def suma_ascii(self, mensaje, inicio=0, paso=1):
        """Suma valores ASCII y retorna una suma total"""
        suma = 0
        while inicio < len(mensaje):
            suma += ord(mensaje[inicio])
            inicio += paso
        return suma

    def suma_verhoeff(self, array_data):
        """Suma un array verhoeff y retorna la suma"""
        suma = 0
        for data in array_data:
            suma = suma + int(data)
        return suma

    def tratar_verhoeff(self, verhoeff):
        """Retorna un array por medio del valor verhoeff aumentando 1 a cada valor"""
        cifra = []
        for actual in verhoeff:
            cifra.append(int(actual)+1)
        return cifra

    def tratar_dosificacion(self, llave_dosificacion, cifra_verhoeff):
        """Retorna un array por medio de la llave de dosificacion y el valor verhoeff """
        cifra = []
        inicio = 0
        for position in cifra_verhoeff:
            final = inicio + position
            cifra.append(llave_dosificacion[inicio:final])
            inicio = final
        return cifra

    def generar_verhoeff_concatenado(self, array_data, cadena_array_verhoeff):
        """Por medio de una cadena de datos de array y una cadena verhoeff, retorna una cadena"""
        cadena = ""
        for actual in range(len(array_data)):
            cadena = cadena + array_data[actual] + cadena_array_verhoeff[actual]
        return cadena

    def generar_qr(self,
                   nit_emisor,
                   numero_factura,
                   numero_autorizacion,
                   fecha_emision,
                   total,
                   importe_base,
                   codigo_control,
                   nit_comprador,
                   importe_ice_iehd_tasas=0,
                   importe_ventas_gravada=0,
                   importe_no_credito_fiscal=0,
                   descuentos=0):
        """Retorna una imagen en BASE64 JPEG"""
        cadena_qr = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % \
                    (nit_emisor,
                     numero_factura,
                     numero_autorizacion,
                     fecha_emision,
                     total,importe_base,
                     codigo_control,
                     nit_comprador,
                     importe_ice_iehd_tasas,
                     importe_ventas_gravada,
                     importe_no_credito_fiscal,
                     descuentos)

        qr_base = qrcode.make(cadena_qr)
        buffer_string = cStringIO.StringIO()
        qr_base.save(buffer_string, format="JPEG")
        qr64 = base64.b64encode(buffer_string.getvalue())
        return qr64