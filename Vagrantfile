# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/bionic64"
  config.vm.box_check_update = false

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    sudo -E apt-get -y update
    sudo -E apt-get -y dist-upgrade
    sudo -E apt-get -y install git build-essential python3-dev python3-pip python3-venv mysql-server libmysqlclient-dev
  SHELL

  config.vm.synced_folder ".", "/home/vagrant/kodingbnx", type: "rsync", rsync__exclude: ".git/"

end
