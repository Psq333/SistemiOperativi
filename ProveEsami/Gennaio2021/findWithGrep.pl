#! /bin/perl

die "Inserire solo argomenti richiesti." if(scalar(@ARGV) != 3);

$path = shift || die "Inserire Path";
$int_D = shift || die "Inserire Int";
$string_S = shift || die "Inserire String";

print "Non intero" if($int_D !~ /\d/);

%hash;
chdir @path;
@output = qx{tree -s};
print(@output);
$cont = 0;
for(@output){
    if(/\s*(\d+)]\s*(.*$string_S.*)/){
        if($1 >= $int_D*1000000){
            $hash{$2} = $1;
            $cont += $1/1000000;      
        }
    } 
}

open($fh, >, "results.out");

for $keys (keys %hash){
    for $value ($hash{$keys}){
        print $fh "$keys $value\n";
    }
}

print "Spazio totale occupato: $cont" 

close($fh);