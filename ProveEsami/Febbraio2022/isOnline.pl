#! /bin/perl

die "Inserisci solo il path" if(scalar(@ARGV) != 1);

$path = shift || die "Elemento non trovato";

@output = qx{arp -an};
%hash = {};
%hash_file = {};

open($fh, "<", "file.txt");

while(<$fh>){
    if(/(.*)#(.*)/){
        $hash_file{$1} = $2;
        print "$2";
    }
}

for (@output){
    if(/\? \((\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3})\) associato a (.*:.*:.*:.*:.*:.*) \[.*/){
        $hash{$1} = $2;
    }
}

%hash_online = {};

for $ip (keys %hash){
    @ping = qx{ping -c1 $ip};
    $bool = 1;
    print("@ping\n");
    for(@ping){
        if(/100% packet loss/){
            $bool = 0;
        }
    }
    if($bool){
        print("offline\n");
        $hash_online{$ip} = "offline";
    }
    else{
        print("online\n");
        $hash_online{$ip} = "online";
    }
}

%hash_finale = {};
for $online(keys %hash_online){
    $primo = $hash{$online};
    $secondo = $hash_file{$primo};
    $hash_finale{$secondo} = $hash_online{$online};
    print ("----$secondo $hash_finale{$secondo}\n");
}
for $key (keys %hash_finale){
    print("$key\n");
}
%hash_finale = sort{($a cmp $b)|| ($hash{$a} cmp $hash{$b}) } keys %hash_finale;



close($fh);