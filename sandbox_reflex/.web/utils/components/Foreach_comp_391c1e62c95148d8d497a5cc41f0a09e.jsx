
import {Fragment,memo,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {Badge as RadixThemesBadge,Button as RadixThemesButton,Flex as RadixThemesFlex,Table as RadixThemesTable,Text as RadixThemesText,Tooltip as RadixThemesTooltip} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_391c1e62c95148d8d497a5cc41f0a09e = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_usuarios____usuario_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state_usuarios____usuario_state.usuarios_rx_state_ ?? [],((u_rx_state_,index_35a310c8a51b4381c42699c5998ed4c3)=>(jsx(RadixThemesTable.Row,{key:index_35a310c8a51b4381c42699c5998ed4c3},jsx(RadixThemesTable.Cell,{},jsx(RadixThemesText,{as:"p",weight:"bold"},u_rx_state_?.["username"])),jsx(RadixThemesTable.Cell,{},u_rx_state_?.["nome_completo"]),jsx(RadixThemesTable.Cell,{align:"center"},jsx(RadixThemesBadge,{color:((u_rx_state_?.["perfil"]?.valueOf?.() === "ADMIN"?.valueOf?.()) ? "ruby" : "blue")},u_rx_state_?.["perfil"])),jsx(RadixThemesTable.Cell,{align:"right"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",justify:"end",gap:"2"},jsx(RadixThemesTooltip,{content:"Resetar Senha (mudar@123)"},jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.reset_password", ({ ["user_id"] : u_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\ud83d\udd11")),jsx(RadixThemesTooltip,{content:"Editar Usu\u00e1rio"},jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.open_edit_user", ({ ["user_dict"] : u_rx_state_ }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u270f\ufe0f")),jsx(RadixThemesTooltip,{content:"Excluir Usu\u00e1rio"},jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.delete_usuario", ({ ["user_id"] : u_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\ud83d\uddd1\ufe0f"))))))))
    )
});
