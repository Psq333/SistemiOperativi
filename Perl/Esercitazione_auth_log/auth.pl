# !usr/bin/Perl

# ./auth.pl [-ip|-user username] name_file

#perl auth.pl -user lyssa auth.log
#perl auth.pl -ip auth.log

$command  = $ARGV[0] || die "Manca primo valore";

%ip_map;

if ($command eq "-ip"){
    $nome_file = $ARGV[1] || die "Manca secondo valore";
    open(fh, '<', $nome_file) || die "Impossibile aprire file";
    print ("Comando: $command sul file: $nome_file\n");
    while (<fh>){
        if(/.*? Failed password for invalid user (.*?) from (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) /){
            $ip_map{$2} += 1;
        }
    }
    while ( ($k,$v) = each %ip_map ) {
       print "$k - $v\n";
    }
    close(fh);
}
elsif ($command eq "-user") {
    $utente = $ARGV[1] || die "Manca secondo valore";
    $nome_file = $ARGV[2] || die "Manca terzo valore";
    open(fh, '<', $nome_file) || die "Impossibile aprire file";
    print ("Comando: $command sul file: $nome_file\n");
    while (<fh>){
        @date;
        if(/(.*? \d{2}:\d{2}:\d{2}) .*? Failed password for invalid user (.*?) /){
            if ($2 eq $utente){
                push @array, $1;
            }
        }
        
    }
    $len = scalar @array;
    print "$utente - $len\n";
    for (@array){   
        print("\t$_\n");
    }
    close(fh);
}



