# !usr/bin/Perl

open(fh, '<', "passeggeri.txt") || die "Impossibile aprire il file";
#open(fh1, '<', "bus.txt") || die "Impossibile aprire il file";
$fermata = $ARGV[0] || die "Inserire fermata di salita controllore";

@array;
@bus;
print(fh1);
@ferbetti;
$ultimapos = 1;
while(<fh>){
    @array = split / /, $_;
    while($ultimapos != @array[0]){
        push @bus, "_";
        $ultimapos++;
    }
    if(@array[2] <= $fermata){
        push @bus, "_";
    }
    elsif (@array[1] eq "no"){
        push @bus, "x";
    }
    else{
        push @bus, "*";
    }
    push @furbetti, @array[0] if(@array[2] <= $fermata && @array[1] eq "no");
    $ultimapos++;
}

while ($ultimapos != 49){
    push @bus, "_";
    $ultimapos++;
}


print("furbetti: ");
print "@furbetti\n";




open(fh_print, ">", "new_bus.txt");

$len = scalar @bus;
print "$len \n";
print "@bus\n";
for ($i = 1; $i <= $len; $i+1){
    $val = shift @bus;
    print fh_print "$val";
    #print "$i%12\n";
    if($i%12 == 0){
        print fh_print "\n";
    }
    else{
        print fh_print " ";
    }
     print fh_print "\n" if($i == 24);
    $i++;
}
close(fh);
#close(fh1);
close(fh_print);