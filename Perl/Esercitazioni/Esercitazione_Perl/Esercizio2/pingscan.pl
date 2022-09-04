# !usr/bin/Perl

die "Necessità di soli 2 argomenti!" if($#ARGV != 1);
"192.168.5.".$_ for(0..255);

$ip_iniziale = @ARGV[0];
$ip_finale = @ARGV[1];

$ip_iniziale =~ s/\./:/ foreach(1..4);
$ip_finale =~ s/\./:/ foreach(1..4);

@ip_iniziale = split(":","$ip_iniziale");
@ip_finale = split(":","$ip_finale");

@ip_i = @ip_iniziale;
@ip_f = @ip_finale;

sub val{
    if(@_[0] != @_[1]){
        return 255;
    }
    else{
        return @_[2];
    }
}

$ciclato = 0;
sub gia_ciclato{
    if (@_[0] == 1){
        return 0;
    }
    else {
        return @_[1];
        
    }
}

#qx(ping "wikihow.com");


for $val1 (@ip_iniziale[0]..@ip_finale[0]){
    for $val2 (@ip_iniziale[1]..val($val1,$ip_finale[0],$ip_finale[1])){
        for $val3 (@ip_iniziale[2]..val($val2,$ip_finale[1],$ip_finale[2])){
            for $val4 (gia_ciclato($ciclato,@ip_iniziale[3])..val($val3,$ip_finale[2],$ip_finale[3])){
                print "ping $val1.$val2.$val3.$val4";
                @output = qx{ping $val1.$val2.$val3.$val4};
                print "$_ " for(@output);
            }
            $ciclato = 1;
        }
    }
}
