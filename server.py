# -*- coding: utf-8 -*-
import socket
import packets

localIP     = "127.0.0.1"
localPort   = 24105
bufferSize  = 1024

if __name__ == '__main__':
  # Create a datagram socket
  serv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

  # Bind to address and ip
  serv.bind((localIP, localPort))

  bytesAddressPair = serv.recvfrom(bufferSize)
  message = bytesAddressPair[0]
  address = bytesAddressPair[1]

  ba = bytearray([int(message, 16)])

  if ba == packets.association_request_ba:
    print('Accept Association Request')
    serv.sendto(packets.association_response, address)
    serv.sendto(packets.mds_create_event_report, address)

    # mds create event result
    bytesAddressPair = serv.recvfrom(bufferSize)
    # rtsa priority list
    bytesAddressPair = serv.recvfrom(bufferSize)
    # set rtsa priority list
    bytesAddressPair = serv.recvfrom(bufferSize)

    i = 0

    while(True):
      # poll request
      bytesAddressPair = serv.recvfrom(bufferSize)
      bytesAddressPair = serv.recvfrom(bufferSize)

      if (0 == i):
        serv.sendto(packets.rsp_group_1_no_1, address)
        serv.sendto(packets.rsp_group_1_no_2, address)
        serv.sendto(packets.rsp_group_1_no_3, address)
        serv.sendto(packets.rsp_group_1_no_4, address)
        serv.sendto(packets.rsp_group_1_no_5, address)
        serv.sendto(packets.rsp_group_1_no_6, address)
      elif (1 == i):
        serv.sendto(packets.rsp_group_2_no_1, address)
        serv.sendto(packets.rsp_group_2_no_2, address)
        serv.sendto(packets.rsp_group_2_no_3, address)
        serv.sendto(packets.rsp_group_2_no_4, address)
      elif (2 == i):
        serv.sendto(packets.rsp_group_3_no_1, address)
        serv.sendto(packets.rsp_group_3_no_2, address)
        serv.sendto(packets.rsp_group_3_no_3, address)
        serv.sendto(packets.rsp_group_3_no_4, address)
        serv.sendto(packets.rsp_group_3_no_5, address)
        serv.sendto(packets.rsp_group_3_no_6, address)
      else:
        serv.sendto(packets.rsp_group_4_no_1, address)
        serv.sendto(packets.rsp_group_4_no_2, address)
        serv.sendto(packets.rsp_group_4_no_3, address)
        serv.sendto(packets.rsp_group_4_no_4, address)
        serv.sendto(packets.rsp_group_4_no_5, address)
        serv.sendto(packets.rsp_group_4_no_6, address)
        serv.sendto(packets.rsp_group_4_no_7, address)

      i += 1
