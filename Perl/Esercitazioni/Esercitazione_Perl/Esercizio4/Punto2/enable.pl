#! /usr/bin/perl

$user_id = shift @ARGV || die "Inserire user-id";

$file_passwd = "../passwd";
$file_disable_txt = "../Punto1/disabled.txt";
open FH, "<", $file_passwd;
open FH_DISABLE, "<", $file_disable_txt;


@contenuto_passwd;
$i = 0;
$entrato = 0;
while (<FH>){
    @line = split/:/,$_;
    if(/(.*):x:(.*?):/ && $2 == $user_id){
        $user_name = $1;
        print "$1-$2\n"; 
        while(<FH_DISABLE>){
            if(/< (.*) - (.*) >/ && $1 eq $user_name){
                print "$1-$2\n";
                $shell = $2;
                @line[$#line] = $shell;
                push @contenuto_passwd, \@line;
                print "@line[$#line] --> $shell\n";
                $entrato = 1;
            }
        }
    }


    
    $linea = join ':', @line;
    if($entrato == 1){
        $linea = join '', $linea, "\n";
        $entrato = 0;
    }
    push @contenuto_passwd, $linea;
    #print $linea;
}

open FH_WRITER, ">", $file_passwd;

for(@contenuto_passwd){
    print FH_WRITER $_;
}