CFG=/etc/apache2/sites-enabled/000-default.conf
SBGNREST_CFG=/etc/apache2/sites-available/sbgn_rest.conf
echo $SBGNREST_CFG
LINE=`cat $CFG | grep -n "</VirtualHost>" | cut -d":" -f1`
head -n $((LINE-1)) $CFG > $SBGNREST_CFG
echo "\tWSGIDaemonProcess RendererAPI user=www-data group=www-data threads=5\n" >> $SBGNREST_CFG
echo "\tWSGIScriptAlias / /var/sbgn-rest-renderer/api/RendererAPI.wsgi\n" >> $SBGNREST_CFG
echo "\t<Directory /var/sbgn-rest-renderer>\n" >> $SBGNREST_CFG
echo "\t\tWSGIProcessGroup RendererAPI\n" >> $SBGNREST_CFG
echo "\t\tWSGIApplicationGroup %{GLOBAL}\n" >> $SBGNREST_CFG
echo "\t\tRequire all granted\n" >> $SBGNREST_CFG
echo "\t</Directory>" >> $SBGNREST_CFG

tail -n +$LINE $CFG >> $SBGNREST_CFG
cat $SBGNREST_CFG