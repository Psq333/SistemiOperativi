#! /bin/perl

die "Inserire SOLO Opzione e Comando" if(scalar(@ARGV) > 2);

$opzione = shift || die "Inserire Opzione";
$comando = shift || die "Inserire Comando";

@output = qx{$comando --help};

if($comando == "-n"){
    $cont = 0;
    for (@output){
        if(/^\s{2}[^- ]/){
            $cont = $cont + 1;
        }
    }
    print("$cont opzioni brevi\n");
}
elsif($comando == "-o"){
    open(fh1, >, "opzioni_brevi.log") || die "File non aperto";
        for (@output){
            if(/\s{2}(-[^- ])[,\s{1}-[^- ],]* (.+)/){

            }
        }
    
}
