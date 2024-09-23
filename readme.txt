O trabalho foi feito em Python, utilizando multithreads e sockets tcp.

O resultado obtido foi um protocolo que identifica um peer da rede como líder se o id deste é o menor da rede inteira.

No início da execução, o peer tenta conectar-se a todos os peers do arquivo "hosts.txt".

O arquivo "host.txt" deve estar no seguinte formato:
	
	host1 host1_id
	host2 host2_id
	host3 host3_id
	host4 host4_id
	...
	hostN hostN_id

Após isso, ele aguarda requisições de conexão de outros peers.

Caso algum peer da rede caia, todos os outros peers entram em modo urgente, para checar se é necesessário mudar o líder da rede.
Enquanto em modo urgente, cada peer assume a liderança, e envia o próprio id para os outros peers.
Caso o peer receba um id menor que o dele, este que recebeu abdica a liderança.
Após todos receberem o id de todos, haverá um peer que não irá ceder a liderança, este sendo de menor id da rede.

Não é possível que um peer que tenha caído reconecte-se à rede sem que todos os outros também encerrem.
