sudo apt install knockd
sudo apt-get install iptables-persisitent
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j REJECT
sudo systemctl start netfilter-persistent
sudo netfilter-persistent save
sudo netfilter-persistend reload