#! /usr/bin/perl

$mode = $#ARGV;

sub check{

    return 1 if(@_[0] =~/^([0-9A-Fa-f])+$/);
    return 0;
    
}

sub checkInputSingolo{
    if(check(@_[0]) == 1){
        print "Numero esadecimale!\n";
    }
    else {
        print "Il numero non è esadecimale.\n";
    }
}

sub checkInputARGV{
    open FH, ">", "risultati.txt";
    for (@_){
        if(check($_) == 1){
            print FH "Numero $_ è esadecimale\n";
        }
        else {
            print FH "Il numero $_ non è esadecimale\n";
        }
    }
    close(FH);
}

print "MODE ARGV, CONTROLLARE FILE RISULTATI.TXT\n" if ($mode != -1);

if($mode == -1){
    print "Inserire il numero:";
    $numero = <>;
    checkInputSingolo($numero);
}
else{
    checkInputARGV(@ARGV);
}