# !usr/bin/Perl

@gironi = ( 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H');
$nome_file = @ARGV[0] || die "Inserire nome_file nel comando";
open(FH_WRITE,">",$nome_file) || "Impossibile creare il file";
printf FH_WRITE "|";
for (@gironi){
    $path = '../ese2/gironi/girone'. $_. '/risultati.txt';
    print "$path\n";
    open(FH,'<', $path) || die "File non trovato";
    %squadre;
    while(<FH>){
        if(/([a-z]{3})-([a-z]{3})=(\d{1,2})-(\d{1,2})/){
            $sq1 = $1;
            $sq2 = $2;
            $score_sq3 = $3;
            $score_sq4 = $4;
            if($score_sq3 > $score_sq4){
                $squadre{$sq1} += 3;
                $squadre{$sq2} += 0;
            }
            elsif($score_sq3 < $score_sq4){
                $squadre{$sq1} += 0;
                $squadre{$sq2} += 3;
            }
            else {
                $squadre{$sq1} += 1;
                $squadre{$sq2} += 1;
            }
        }
    }
    my @array = sort { $a <=> $b } map $_->{b}, values %squadre;
    $i = 0;
    
    foreach my $name (sort {$squadre{$b} <=> $squadre{$a}} keys %squadre) {
        if ($i == 1){
            printf FH_WRITE "$name |";
            last;
        }
        printf FH_WRITE " $name ";
        $i+=1;
    }

    %squadre = ();

    close(FH);

}
close(FH_WRITE);

