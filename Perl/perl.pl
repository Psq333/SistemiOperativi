#! /bin/perl



open ($fh1 , ">" , "file.txt") || die "morto";


print $fh1 "ciao\n";
print $fh1 "ciao\n";
print $fh1 "ciao\n";
print $fh1 "ciao\n";

close($fh1);

open ($fh1, "<", "file.txt") || die "Non aperto";

while (<$fh1>){
    print("ok");
    print $_;
}
close($fh1);