# -*- coding: utf-8 -*-
import socket
import packets
import time
from multiprocessing import Process

localIP     = "0.0.0.0"
localPort   = 24105
bufferSize  = 1024

def startSendData(serv, clientAddress):
  nu = 0
  wa = 0
  address = clientAddress

  while(True):
    # poll request
    print('Waiting poll request')
    serv.settimeout(10)
    bytesAddressPair = serv.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    if (len(message) > 34):
      if (message[33] == 0x06):
        # numeric
        print('accept poll request of numeric')
        if (0 == nu):
          serv.sendto(packets.rsp_nu_1_no_1, address)
          serv.sendto(packets.rsp_nu_1_no_2, address)
          serv.sendto(packets.rsp_nu_1_no_3, address)
        elif (1 == nu):
          serv.sendto(packets.rsp_nu_2_no_1, address)
          serv.sendto(packets.rsp_nu_2_no_2, address)
          serv.sendto(packets.rsp_nu_2_no_3, address)
        elif (2 == nu):
          serv.sendto(packets.rsp_nu_3_no_1, address)
          serv.sendto(packets.rsp_nu_3_no_2, address)
          serv.sendto(packets.rsp_nu_3_no_3, address)
        else:
          serv.sendto(packets.rsp_nu_4_no_1, address)
          serv.sendto(packets.rsp_nu_4_no_2, address)
          serv.sendto(packets.rsp_nu_4_no_3, address)
        nu += 1
        nu = nu % 4
      elif (message[33] == 0x09):
        # wave
        print('accept poll request of wave')
        if (0 == wa):
          serv.sendto(packets.rsp_wave_1_no_1, address)
        elif (1 == wa):
          serv.sendto(packets.rsp_wave_2_no_1, address)
        elif (2 == wa):
          serv.sendto(packets.rsp_wave_3_no_1, address)
          serv.sendto(packets.rsp_wave_3_no_2, address)
          serv.sendto(packets.rsp_wave_3_no_3, address)
        else:
          serv.sendto(packets.rsp_wave_4_no_1, address)
          serv.sendto(packets.rsp_wave_4_no_2, address)
          serv.sendto(packets.rsp_wave_4_no_3, address)
          serv.sendto(packets.rsp_wave_4_no_4, address)
        wa += 1
        wa = wa % 4

def startListen(serv):
  print('Waiting association request')
  serv.settimeout(None)
  bytesAddressPair = serv.recvfrom(bufferSize)
  try:
    serv.settimeout(10)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    ba = bytearray(message)

    if ba == packets.association_request_ba:
      print('Accept Association Request')
      serv.sendto(packets.association_response, address)
      serv.sendto(packets.mds_create_event_report, address)

      # mds create event result
      print('Waiting mds create event result')
      bytesAddressPair = serv.recvfrom(bufferSize)
      # rtsa priority list
      print('Waiting rtsa priority list')
      bytesAddressPair = serv.recvfrom(bufferSize)
      # set rtsa priority list
      print('Waiting set rtsa priority list')
      bytesAddressPair = serv.recvfrom(bufferSize)

      serv.sendto(packets.rsp_get_result, address)
      serv.sendto(packets.rsp_confirmed_set_result, address)

      startSendData(serv, address)
  except socket.timeout:
    print('timeout')
  else:
    print('Unknown Error')


if __name__ == '__main__':
  # Create a datagram socket
  serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

  # Bind to address and ip
  serv.bind((localIP, localPort))

  while(True):
    startListen(serv)
    time.sleep(3)
