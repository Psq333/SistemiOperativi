#! /usr/bin/perl

die "Servono solo 2 nomi dei file" if($#ARGV != 1);
$file_output = shift @ARGV;
$file_passwd = shift @ARGV;
print "$file_output -> $file_passwd";

open FH, "<", $file_output || die "Impossibile aprire il file.";


%accessi;
@bannati;
sub presente{
    $val = @_[0];
    for(@bannati){
        if ($_ eq @_[0]){
            return 0;
        }
    }
    return 1;
}

for $line (<FH>){
    if ($line =~ /([a-zA-Z]{3} \d{2}) .* authentication failure.* user=(.*)/){
        $data = $1;
        $user = $2;
        $accessi{$data}{$user} += 1;
        #print "$data $user $accessi{$data}{$user}\n";
    }
}


close FH;


for $ext (values %accessi){
    for $key(keys %{$ext}){
       #print "$key --> ${$ext}{$key}\n";
       $val = presente($key);
       if( $val == 1 && ${$ext}{$key} >= 2){
            push @bannati, $key;
       }
    }
}


print ("\n");
print("$_ ") for (@bannati);
print ("\n");

$file_disabled_txt = "disabled.txt";

open FH_READER, "<", $file_passwd || die "Impossibile aprire il file.";
open FH_WRITER_TXT, ">", $file_disabled_txt || die "Impossibile aprire il file.";

$stringa = "/bin/alert.sh\n";
%contenuto_passwd;
$i = 0;
while (<FH_READER>){
    @line = split/:/,$_;
    if(presente(@line[0]) == 0){
        chomp @line[$#line];
        print FH_WRITER_TXT "< @line[0] - @line[$#line] >\n";
        print "< @line[0] - @line[$#line] >\n";
        @line[$#line] = $stringa;
    }
    $contenuto_passwd{$i} = [@line];
    $i+=1 
}

close FH_WRITER_TXT;
close FH_READER;

open FH_WRITER, ">", $file_passwd || die "Impossibile aprire il file.";
for (keys %contenuto_passwd){
    $val = join ':', @{$contenuto_passwd{$_}};
    print FH_WRITER $val;
}

close FH_WRITER;