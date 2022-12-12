if [ -e /usr/local/bin/node_exporter ]
then
    echo "exporter is available, skipping installation at $(hostname)"
else
    OS=`awk -F= '$1=="ID_LIKE" { print $2 ;}' /etc/os-release`

    # file at /tmp/
    tar -xvf /tmp/node_exporter.tar.gz --directory /tmp/
    useradd -rs /bin/false node_exporter
    rm /etc/systemd/system/node_exporter.service -f

    cat <<EOF>/tmp/node_exporter.service
    [Unit]
    Description=Node Exporter
    After=network.target
    [Service]
    User=node_exporter
    Group=node_exporter
    Type=simple
    ExecStart=/usr/local/bin/node_exporter
    [Install]
    WantedBy=multi-user.target
EOF

    case "$OS" in
        "fedora"|fedora|"rhel fedora")
            echo "found fedora"
            sudo cp -Z /tmp/node_exporter-1.5.0.linux-amd64/node_exporter /usr/local/bin/
            sudo cp -Z /tmp/node_exporter.service /etc/systemd/system/node_exporter.service
            ;;
        "debian"|debian)
            echo "found debian"
            sudo cp /tmp/node_exporter-1.5.0.linux-amd64/node_exporter /usr/local/bin/
            sudo cp /tmp/node_exporter.service /etc/systemd/system/node_exporter.service
            ;;
        *)
            echo "os type not found, default copy selected"
            sudo cp /tmp/node_exporter-1.5.0.linux-amd64/node_exporter /usr/local/bin/
            sudo cp /tmp/node_exporter.service /etc/systemd/system/node_exporter.service
            ;;
    esac

    timedatectl set-timezone Asia/Jakarta
    systemctl daemon-reload
    systemctl start node_exporter
    systemctl enable node_exporter
    systemctl status node_exporter
    echo "Install node exporter done"
fi
