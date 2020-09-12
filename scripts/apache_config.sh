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
echo "\tAlias /node_modules \"/var/sbgn-rest-renderer/node_modules/\"\n" >> $SBGNREST_CFG
echo "\t<Directory \"/var/www/node_modules\">\n" >> $SBGNREST_CFG  
echo "\t\tOptions +Indexes\n" >> $SBGNREST_CFG
echo "\t\tAllowOverride None\n" >> $SBGNREST_CFG
echo "\t\tOrder allow,deny\n" >> $SBGNREST_CFG
echo "\t\tAllow from all\n" >> $SBGNREST_CFG
echo "\t</Directory>\n\n" >> $SBGNREST_CFG

echo "\tAlias /app \"/var/sbgn-rest-renderer/app/\"\n" >> $SBGNREST_CFG
echo "\t<Directory \"/var/www/app\">\n" >> $SBGNREST_CFG
echo "\t\tOptions +Indexes\n" >> $SBGNREST_CFG
echo "\t\tAllowOverride None\n" >> $SBGNREST_CFG
echo "\t\tOrder allow,deny\n" >> $SBGNREST_CFG
echo "\t\tAllow from all\n" >> $SBGNREST_CFG
echo "\t</Directory>\n" >> $SBGNREST_CFG




tail -n +$LINE $CFG >> $SBGNREST_CFG
cat $SBGNREST_CFG