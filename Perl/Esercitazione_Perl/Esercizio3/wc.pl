#! /usr/bin/perl

$mode = shift || die "Modalità non presente";

if ($mode eq "-l"){
    $nome_file = shift || die "Nome file non presente";
    open FH, "<", $nome_file || die "Impossibile aprire file!";
    print "Comando: $mode\n";
    $cont_righe = 0;
    while(<FH>){
        $cont_righe+=1;
    }
    print "Righe del file $nome_file sono $cont_righe\n";
}
elsif ($mode eq "-w" || $#ARGV == -1){
    $nome_file = $mode if($#ARGV == -1);
    $nome_file = shift || die "Nome file non presente" if ($#ARGV == 0);
    open FH, "<", $nome_file || die "Impossibile aprire file!";
    print "Comando: $mode\n";
    $num = 0;
    while (<FH>){
        @array = split/[ .,;:\-\s]/,$_;
        for $x (@array){
            $num += 1;
        }
    }
    print "Numero parole $num\n";
}
elsif ($mode =~ /-w=(.*)/){
    $nome_file = shift || die "Nome file non presente";
    open FH, "<", $nome_file || die "Impossibile aprire file!";
    print "Comando: $mode\n";
    $word = $1;
    $cont_word = 0;
    while(<FH>){
        chomp $_;
        @line = split/[ .,;:\-\s]/, $_;
        for (@line){
            if($_ eq $word){
                #print "paragone $_ eq $word\n";
                $cont_word += 1;
            }
        }
    }
    print "Ci sono $cont_word instanze della parola $word";
}
else{
    print "Modalità non esistente";
}
close(FH);