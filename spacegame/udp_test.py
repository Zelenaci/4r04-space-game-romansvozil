import spacegame
import threading, time


#funkce, které nám budou na pozadí vypisovat příchozí zprávu
def server_print():
    while True:
        if server.data_received == []:
            pass
        else:
            print('{0}: {1}'.format(server.connected_client[1], server.data_received[0].decode()))
            server.data_received.remove(server.data_received[0])

def client_print():
    while True:
        if client.data_received == []:
            pass
        else:
            print('{0}: {1}'.format(client.connected_to, client.data_received[0].decode()))
            client.data_received.remove(client.data_received[0])

#prvně si definujeme mod, buď server nebo client
mode = int(input('0 - client \n1 - server \n'))

#pokud vybereme clienta
if mode == 0:

    #nazačátek si pojmenujeme clienta
    client_name = input('Client name(1 word): ')

    #vytvoříme objekt client, který sám o sobě nevytváří žádné thready ani sockety
    client = spacegame.udp_client.Client(client_name)

    #vytvoříme thread, který vytvoří socket a bindne ho na broadcast s PORTEM z configu
    client.find_server_thread = threading.Thread(target=client.broadcast_find_server).start()

    #dokud nám 'client.find_server_thread' nenajde žádný aktivní server čekáme a kontrolujeme co 1.5 s
    while client.found_servers == {}:
        time.sleep(1.5)

    #po tom co najdeme server vypneme socket, který 'poslouchal' na broadcastu a thread dokončí funkci
    client.broadcast_socket.close()

    #pro případ, že bude na broadcastu vysílat více serverů naší hry, tak si sami vybereme server
    client.connected_to = input('{}\n'.format(client.found_servers))

    #vytvoříme finální thread, který se bude starat o přímou komunikaci se serverem
    client.client_thread = threading.Thread(target=client.client_start, args=(client.found_servers[client.connected_to],)).start()

    #pro demonstraci vytvoříme thread, který nám bude vypisovat příchozí data
    print_thread = threading.Thread(target=client_print).start()

    #cyklus, ve kterém zapisujeme data, která chceme odeslat serveru
    while True:
        data = input()
        client.data_to_send.append(data)

#pokud vybereme server
elif mode == 1:

    #nazačátek si pojemenujeme server
    server_name = input('Server name(1 word): ')

    #vytvoříme objekt server, který sám o sobě nevytváří žádné thready ani sockety
    server = spacegame.udp_server.Server(server_name)

    #vytvoříme thread se socketem, který bude každou vteřinu posílat na broadcast data
    #ve stylu 'spacegame *jméno_serveru*', slova 'spacegame' si vyšimne client a do slovníku
    #si pod klíčem *jméno_serveru* uloží IP adresu serveru, zároveň však musíme vytvořit thread
    #který se bude starat o přijímání a odesílání dat. První data, která příjdou od clienta
    #je jméno clienta, díky čemuž je server schopen si uložit IP adresu a PORT clienta pod jeho jménem
    server.find_server_thread = threading.Thread(target=server.broadcast_find_client).start()
    server.server_thread = threading.Thread(target=server.server_start).start()

    #čekáme než se připojí první klient.. Jak jste si mohli všimnout, tak server je zatím
    #designován tak, aby po připojení 1. clienta ihned vypnul socket. Tudiž se může připojit
    #pouze jeden client
    while server.connected_client == []:
        pass

    server.broadcast_socket.close()

    #znovu pouze demonstrační thread pro vypisování příjmutých dat
    print_thread = threading.Thread(target=server_print).start()

    #nekonečná smyčka pro odesílání dat
    while True:
        data = input()
        server.data_to_send.append(data)
