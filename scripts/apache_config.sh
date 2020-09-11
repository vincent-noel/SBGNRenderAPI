CFG=/etc/apache2/sites-enabled/000-default.conf
SBGNREST_CFG=/etc/apache2/sites-available/sbgn_rest.conf
echo $SBGNREST_CFG
LINE=`cat $CFG | grep -n "</VirtualHost>" | cut -d":" -f1`
head -n $((LINE-1)) $CFG > $SBGNREST_CFG
echo "\tWSGIDaemonProcess RendererAPI user=www-data group=www-data threads=5\n\tWSGIScriptAlias / /var/sbgn-rest-renderer/api/RendererAPI.wsgi\n\t<Directory /var/sbgn-rest-renderer>\n\t\tWSGIProcessGroup RendererAPI\n\t\tWSGIApplicationGroup %{GLOBAL}\n\t\tRequire all granted\n\t</Directory>" >> $SBGNREST_CFG
tail -n +$LINE $CFG >> $SBGNREST_CFG
cat $SBGNREST_CFG