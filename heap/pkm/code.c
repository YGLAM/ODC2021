typedef unsigned char   undefined;

typedef unsigned char    byte;
typedef unsigned char    dwfenc;
typedef unsigned int    dword;
typedef unsigned long    qword;
typedef unsigned int    uint;
typedef unsigned long    ulong;
typedef unsigned long long    ulonglong;
typedef unsigned char    undefined1;
typedef unsigned int    undefined4;
typedef unsigned long    undefined8;
typedef unsigned short    ushort;
typedef unsigned short    word;
typedef struct struct_move struct_move, *Pstruct_move;

struct struct_move {
    char * name;
    void (* function)(undefined8 *, undefined *);
};

typedef struct struct_pkm struct_pkm, *Pstruct_pkm;

struct struct_pkm {
    ulonglong atk;
    ulonglong def;
    ulonglong hp;
    ulonglong max_hp;
    char status;
    char * name;
    ulonglong IVs[5];
    struct struct_move move[10];
};
void tackle(undefined8 *tackler_atk,long pkmn_2){
  uint dmg;

  dmg = (int)*tackler_atk - (int)*(undefined8 *)(pkmn_2 + 8);//this should be the def
  if ((int)dmg < 0) {
    dmg = 0;
  }
  *(long *)(pkmn_2 + 0x10) = *(long *)(pkmn_2 + 0x10) - (long)(int)dmg;//is this the hp ?
  if ((int)dmg < 1) {
    printf("[%%] %s is safe!\n",*(undefined8 *)(pkmn_2 + 0x28));
  }
  else {
    printf("[%%] %s loses %d hp\n",*(undefined8 *)(pkmn_2 + 0x28),(ulong)dmg);
  }
  return;
}
void * get_string(void){
  long in_FS_OFFSET;
  uint length;
  uint index;
  void *zone;
  long canary;

  canary = *(long *)(in_FS_OFFSET + 0x28);
  length = 0;
  while (length == 0) {
    printf("[.] insert length: ");
    __isoc99_scanf(&DAT_0040204e,&length);
  }
  zone = malloc((ulong)length);
  index = 0;
  while ((index < length &&
         (read(0,(void *)((long)zone + (ulong)index), 1 ),
         *(char *)((long)zone + (ulong)index) != '\n'))) {
    index = index + 1;
  }
  *(undefined *)((long)zone + (ulong)index) = 0;//THIS IS THE NULL BYTE POISONING
  if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
    return zone;
  }
                    // WARNING: Subroutine does not return
  __stack_chk_fail();
}
struct_pkm * new_pkm(void){
  long lVar1;
  fun_move *basic_move;
  struct_pkm *pkm_addr;
  byte index;

  pkm_addr = (struct_pkm *)malloc(248);//0xf8
  // ???
  *(undefined **)((long)&pkm_addr->name + 7) = UNKNOWN;
  //Base Stats
  pkm_addr->atk = 40;
  pkm_addr->def = 10;
  pkm_addr->hp = 100;
  pkm_addr->max_hp = 100;
  //Moves, I'm setting up tackle as a basic move
  basic_move = TACKLE.function;//here I get the function
  *(char **)((long)&pkm_addr->move[0].name + 7) = TACKLE.name;//Here I inject the name
  *(fun_move **)((long)&pkm_addr->move[0].function + 7) = basic_move;//here I inject the function call

  for (index = 0; basic_move = M_EMPTY.function, index < 10; index++) {
//here I'm setting up the IVs or are those the moves ?I think these are the moves
    lVar1 = (long)pkm_addr->IVs + (long)(int)(uint)index * 0x10 + 0x27;
    *(char **)(lVar1 + 8) = M_EMPTY.name;
    *(fun_move **)(lVar1 + 16) = basic_move;
  }
  return pkm_addr;
}
void add_pkm(void){
  undefined8 pkm;
  byte index;

  puts("[*] New PKM!");
  index = 0;
  while ((index < 50 && (pkms[(int)(uint)index] != 0))) {
    index++;
  }
  if (index == 50) {
    puts("[!] No more free slots for pkms");
  }
  else {
    pkm = new_pkm();
    pkms[(int)(uint)index] = pkm;
    *(ulong *)(pkms[(int)(uint)index] + 0x30) = (ulong)index;//48=0x30
  }
  return;
}
void print_pkm_list(void){
  byte index;
  for (index = 0; index < 0x32; index++) {//0x32=50
    if (pkms[(int)(uint)index] != 0) {
      printf("[%d] %s\n",(ulong)index,*(undefined8 *)(pkms[(int)(uint)index] + 0x28));
    }
  }
  return;
}

byte get_pkm(void){
  long in_FS_OFFSET;
  byte desired_pkm_index;
  long canary;

  canary = *(long *)(in_FS_OFFSET + 0x28);
  do {
    puts("[*] Choice a PKM!");
    print_pkm_list();
    printf("> ");
    __isoc99_scanf(&DAT_0040209e,&desired_pkm_index);
    if (pkms[(int)(uint)desired_pkm_index] != 0) break;
  } while (desired_pkm_index < 50);

  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    // WARNING: Subroutine does not return
    __stack_chk_fail();
  }
  return desired_pkm_index;
}

void rename_pkm(void){
  long pkm;
  byte pkm_index;
  undefined8 name;

  puts("[*] Rename PKM!");
  pkm_index = get_pkm();
  if ((*(long *)(pkms[(int)(uint)pkm_index] + 0x28) != 0) &&
     (*(undefined **)(pkms[(int)(uint)pkm_index] + 0x28) != UNKNOWN)) {
    free(*(void **)(pkms[(int)(uint)pkm_index] + 0x28));//If the name is not 0 or UNKNOWN I free it
  }
  pkm = pkms[(int)(uint)pkm_index];
  name = get_string();
  *(undefined8 *)(pkm + 0x28) = name;
  return;
}

void del_pkm(byte index){
  int name_off = 0x28
  if (pkms[(int)(uint)index] != 0) {
    if ((*(long *)(pkms[(int)(uint)index] + name_off) != 0) && //Verifies the state of the name pointer
       (*(undefined **)(pkms[(int)(uint)index] + name_off) != UNKNOWN)) {
      free(*(void **)(pkms[(int)(uint)index] + name_off));//If it isn't free it frees it !!
    }
    free((void *)pkms[(int)(uint)index]);//then it frees the pokemon itself
  }
  pkms[(int)(uint)index] = 0;//and makes the entry point to null
  return;
}
void delete_pkm(void){
  undefined pkm_id;

  puts("[*] Delete PKM!");
  pkm_id = get_pkm();
  del_pkm(pkm_id);
  return;
}
void print_moves(byte id){
  byte index;
  undefined8 *pkm;

  pkmn = (undefined8 *)pkms[ (int)(uint)id ];
  if (pkmn != (undefined8 *)0x0) {
    for (; index < 10; index++ ) {
      if (pkmn[((long)(int)(uint)index + 5) * 2 + 2] != 0) {
        printf("\t(%d) %s\n",(ulong)index , pkmn[((long)(int)(uint)index + 5) * 2 + 1]);
      }
    }
  }
  return;
}
long get_move(byte id){
  long in_FS_OFFSET;
  byte index;
  long canary;

  canary = *(long *)(in_FS_OFFSET + 0x28);
  do {
    puts("[*] Choice a Move!");
    print_moves(id);
    printf("> ");
    //I choose which move I'll play
    __isoc99_scanf(&DAT_0040209e,&index);
    if (*(long *)(((long)(int)(uint)index + 5) * 16 + pkms[(int)(uint)id] + 16) != 0) break;
    //this thing somehow points to a move ?
  } while (index < 10);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    // WARNING: Subroutine does not return
    __stack_chk_fail();
  }
  return ((long)(int)(uint)index + 5) * 16 + pkms[(int)(uint)id] + 8;//I'm returning the move
  //It will be casted as a pointer later
}

void fight_pkm(void){
  byte pkm_id_1;
  byte pkm_id_2;
  undefined8 *move;

  puts("[*] Fight PKMs!");
  pkm_id_1 = get_pkm();
  move = (undefined8 *)get_move(pkm_id_1);
  pkmn_id_2 = get_pkm();
  //actual move
  printf("[%%] %s uses %s on %s!\n",
          *(undefined8 *)(pkms[(int)(uint)pkm_id_1] + 0x28) //name
          ,*move, // his move name
          *(undefined8 *)(pkms[(int)(uint)pkm_id_2] + 0x28));//name of the foe
  //calling the actual move
  (*(code *)move[1])//this is move.name
            (pkms[(int)(uint)pkm_id_1] ,
             pkms[(int)(uint)pkm_id_2] ,
             pkms[(int)(uint)pkm_id_2] ,
             (code *)move[1]);//these are the arguments of the function call
  //I check if the opponent's pkm has fainted
  death_checker(pkmn_id_2);
  return;
}
void death_checker(byte id){
  if (*(long *)(pkms[(int)(uint)id] + 16) == 0) {
    printf("[!!!] %s fainted!\n",*(undefined8 *)(pkms[(int)(uint)id] + 40));
    del_pkm(id);//If the pkm has fainted I delete him :(
  }
  return;

}
void info_pkm(void){
  undefined8 *pkmn;
  byte pkm_id;
  byte index;

  puts("[*] Info PKMs!");
  pkm_id = get_pkm();
  pkmn = (undefined8 *)pkms[(int)(uint)pkm_id];
  if (pkmn[5] != 0) {
    printf(" *Name: %s\n",pkmn[5]);
  }
  printf(" *ATK:  %d\n",*pkmn);
  printf(" *DEF:  %d\n",pkmn[1]);
  printf(" *HP:   %d/%d\n",pkmn[2],pkmn[3]);//also max hp
  puts(" *Moves:");
  for (; index < 10; index++) {
    if (pkmn[((long)(int)(uint)index + 5) * 2 + 2] != 0) {
      printf("  (%d) %s\n",(ulong)index , pkmn[((long)(int)(uint)index + 5) * 2 + 1]);//13=D
    }
  }
  return;
}
void print_menu(void){
  puts("***************");
  puts("0. Add PKM");
  puts("1. Rename PKM");
  puts("2. Kill PKM");
  puts("3. Fight PKM");
  puts("4. Info PKM");
  puts("5. Exit");
  puts("***************");
  return;
}

void main(void){
  long in_FS_OFFSET;
  byte local_11;
  undefined8 local_10;

  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  alarm(0xffffffff);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  do {
    print_menu();
    printf("> ");
    __isoc99_scanf(&DAT_0040209e,&local_11);
    switch(local_11) {
    case 0:
      add_pkm();
      break;
    case 1:
      rename_pkm();
      break;
    case 2:
      delete_pkm();
      break;
    case 3:
      fight_pkm();
      break;
    case 4:
      info_pkm();
      break;
    case 5:
      exit(0);
    default:
      puts("[!] Wrong choice!");
    }
  } while( true );
}
